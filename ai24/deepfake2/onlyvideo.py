import cv2
import numpy as np
import mediapipe as mp

# Getting facial landmarks from an image
def find_face_landmarks(pic):
    face_mesh = mp.solutions.face_mesh.FaceMesh(max_num_faces=1, 
                                                refine_landmarks=True, 
                                                min_detection_confidence=0.2, 
                                                min_tracking_confidence=0.2)
    pic_height, pic_width = pic.shape[:2]
    landmarks = []
    analysis = face_mesh.process(pic)
    if analysis.multi_face_landmarks:
        for facial_landmarks in analysis.multi_face_landmarks:
            for landmark in facial_landmarks.landmark:
                x, y = int(landmark.x * pic_width), int(landmark.y * pic_height)
                landmarks.append((x, y))
    return landmarks

# Applying affine transformation
def affine_transform(source, srcTri, dstTri, size):
    warp_matrix = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))
    transformed = cv2.warpAffine(source, warp_matrix, (size[0], size[1]), None, 
                                 flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return transformed

# Computing Delaunay triangles
def delaunay_triangles(rect, points):
    subdiv = cv2.Subdiv2D(rect)
    for point in points:
        subdiv.insert(point)
    triangles = subdiv.getTriangleList()
    delaunay_tris = []
    for triangle in triangles:
        pt1, pt2, pt3 = (triangle[0], triangle[1]), (triangle[2], triangle[3]), (triangle[4], triangle[5])
        indices = [points.index(pt1), points.index(pt2), points.index(pt3)]
        delaunay_tris.append(tuple(indices))
    return delaunay_tris

# Warping triangles for animation
def warp_face_triangle(img1, img2, t1, t2):
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    t1_rect, t2_rect = [], []
    for i in range(3):
        t1_rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2_rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2_rect), (1.0, 1.0, 1.0))

    img1_rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    warp_image = affine_transform(img1_rect, t1_rect, t2_rect, (r2[2], r2[3]))

    img2_rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]
    
    # Correctly blend img2_rect with the mask and warp_image
    img2_rect = img2_rect.astype(np.float32) / 255.0  # Convert to float for precise computation
    warp_image = warp_image.astype(np.float32) / 255.0  # Ensure warp_image is also float32 for matching operation
    
    img2_rect = img2_rect * ((1.0, 1.0, 1.0) - mask) + warp_image * mask
    img2_rect = (img2_rect * 255).astype(np.uint8)  # Convert back to uint8 for image representation

    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2_rect
    return img2


# Animate the face based on movements
def animate_face(static_image, movements):
    img_height, img_width = static_image.shape[:2]
    animated_images = []
    base_landmarks = find_face_landmarks(static_image)
    for movement in movements:
        frame = static_image.copy()
        for base, move in zip(base_landmarks, movement):
            adjusted_landmarks = [(base[0] + move[0], base[1] + move[1]) for base, 
                                  move in zip(base_landmarks, movement)]
        delaunay_tris = delaunay_triangles((0, 0, img_width, img_height), base_landmarks)
        for tri in delaunay_tris:
            x, y, z = tri
            t1 = [base_landmarks[x], base_landmarks[y], base_landmarks[z]]
            t2 = [adjusted_landmarks[x], adjusted_landmarks[y], adjusted_landmarks[z]]
            frame = warp_face_triangle(static_image, frame, t1, t2)
        animated_images.append(frame)
    return animated_images

# Save the animated frames to a video
def save_video(frames, output_file="animated_faces.mp4"):
    frame_height, frame_width = frames[0].shape[:2]
    video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MP4V'), 20, (frame_width, frame_height))
    for frame in frames:
        video_writer.write(frame)
    video_writer.release()

# Main process
video_path = "input/input.mp4"
static_img_path = "input/face2.jpg"
video_capture = cv2.VideoCapture(video_path)
static_img = cv2.imread(static_img_path)
movements = []

while True:
    success, frame = video_capture.read()
    if not success:
        break
    movements.append(find_face_landmarks(frame))

video_capture.release()

# Animate and save
animated_frames = animate_face(static_img, movements)
save_video(animated_frames, "out2/final_animation.mp4")
print("Animation complete!")
