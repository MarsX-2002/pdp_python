import cv2
import numpy as np
import mediapipe as mp



# From workshop given by our mentor
# it is greatly edited by me
def get_landmarks(image):

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.2,
        min_tracking_confidence=0.2,
        
    )
    image_height, image_width = image.shape[:2]
    # image.shape -> (image_height, image_width, channels)

    landmark_points = []

    
    results = face_mesh.process(image)

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            for landmark in face_landmarks.landmark:
                # [(0.343, 0.43) .. ]
                x, y = int(landmark.x * image_width), int(landmark.y * image_height)
                landmark_points.append((x,y))
            



    return landmark_points

# From workshop given by our mentor
def apply_affine_transform(src, srcTri, dstTri, size):
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))
    dst = cv2.warpAffine(src, warpMat, (size[0], size[1]), None,
                         flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return dst

# From workshop given by our mentor
def compute_delaunay_triangles(rect, points):
    subdiv = cv2.Subdiv2D(rect)
    for p in points:
        subdiv.insert(p)
    triangle_list = subdiv.getTriangleList()
    delaunay_tri = []

    for t in triangle_list:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        ind1 = points.index(pt1)
        ind2 = points.index(pt2)
        ind3 = points.index(pt3)
        delaunay_tri.append((ind1, ind2, ind3))

    return delaunay_tri


# From workshop given by our mentor
def warp_triangle(img1, img2, t1, t2):
    # img1 -> static_img
    # img2 -> frame

    # initial point's rectangle
    r1 = cv2.boundingRect(np.float32([t1]))
    # print(f"r1: {r1}")

    # adjusted point's rectangle
    r2 = cv2.boundingRect(np.float32([t2]))
    # print(f"r1: {r1}")

    t1Rect = []
    t2Rect = []
    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))

    mask = np.zeros((r2[3], r2[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2Rect), (1.0, 1.0, 1.0), 16, 0)

    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    size = (r2[2], r2[3])
    size = (int(r2[2]), int(r2[3]))
    warpImage = apply_affine_transform(img1Rect, t1Rect, t2Rect, size)

    warpImage = warpImage * mask

    img2Rect = img2[r2[1]:r2[1] + size[1], r2[0]:r2[0] + size[0]]

    img2Rect = img2Rect * ((1.0, 1.0, 1.0) - mask)

    img2[r2[1]:r2[1] + size[1], r2[0]:r2[0] + size[0]] = img2Rect + warpImage

    # cv2.imshow("img2", img2)
    # cv2.waitKey(1)
    return img2

def calculate_relative_movements(initial_landmarks, movements):

    static_img_convexhull = cv2.convexHull(np.array(initial_landmarks, np.int32))
    static_img_rect = cv2.boundingRect(static_img_convexhull)




    relative_movements = []
    for frame_landmarks in movements:
        relative_frame_movements = []

        frame_convexhull = cv2.convexHull(np.array(frame_landmarks, np.int32))
        frame_face_rect = cv2.boundingRect(frame_convexhull)


        ratio_width = (frame_face_rect[2] / static_img_rect[2])

        ratio_height = (frame_face_rect[3] / static_img_rect[3])
        expression_killer_rate = 3


        for i, (initial_point, current_point) in enumerate(zip(initial_landmarks, frame_landmarks)):
            

            movement = (((current_point[0]- frame_face_rect[0])/ratio_width - (initial_point[0] - static_img_rect[0]))/expression_killer_rate, 
                        ((current_point[1]- frame_face_rect[1])/ratio_height - (initial_point[1] - static_img_rect[1]))/expression_killer_rate)
            
    
            
            # changing the movement x results in skewing the future frame along x axis
            # changing the movement y results in skewing the future frame along y axis
            
            relative_frame_movements.append(movement)

        relative_movements.append(relative_frame_movements)
    return relative_movements

def animate_face(static_img, movements):
    height, width = static_img.shape[:2]

    animated_frames = []
    initial_landmarks = get_landmarks(static_img)
    relative_movements = calculate_relative_movements(initial_landmarks, movements)
    rect = (0, 0, width, height)

    delaunay_triangles = compute_delaunay_triangles(rect, initial_landmarks)

    for i, frame_movements in enumerate(relative_movements):
        frame = static_img.copy()
        adjusted_landmarks = [(initial_pt[0] + move[0], initial_pt[1] + move[1]) for initial_pt, move in zip(initial_landmarks, frame_movements)]
        print(i)
        for tri_indices in delaunay_triangles:
            x, y, z = tri_indices
            t1 = [initial_landmarks[x], initial_landmarks[y], initial_landmarks[z]]
            t2_x, t2_y, t2_z = (adjusted_landmarks[x], adjusted_landmarks[y], adjusted_landmarks[z])
            t2 = [t2_x, t2_y, t2_z]

            frame = warp_triangle(static_img, frame, t1, t2)

        animated_frames.append(frame)

    return animated_frames

def create_video(frames, output_path="animated_output.mp4"):
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, size)

    for i in range(len(frames)):
        out.write(frames[i])


    

    out.release()


# video_capture = cv2.VideoCapture(0)
input_video_file_name = "input/input"
video_source = cv2.VideoCapture(f"{input_video_file_name}.mp4")
frame_rate = video_source.get(cv2.CAP_PROP_FPS)

static_img = cv2.imread("input/face2.jpg")
frame_width, frame_height = 0, 0
movements = []


while video_source.isOpened():

    ret, frame = video_source.read()
    if not ret:
        break
    
    if not frame_width or not frame_width:
        frame_width, frame_height = frame.shape[:2]

    # if ret == True:
    # getting all the landmarks for each frame by video_source
    
    movements.append(get_landmarks(frame))
    # get_landmarks(frame) -> [468 coordinates (x,y) for each landmark] ->



output_video_file_name = "output/video_without_audio-2"

print("first phase is done!")


animated_frames = animate_face(static_img, movements)
create_video(animated_frames, f"{output_video_file_name}.mp4")
video_source.release()
print("second phase is done!")







import librosa
import soundfile as sf
from moviepy.editor import VideoFileClip, AudioFileClip

video_source = VideoFileClip(f"{input_video_file_name}.mp4")

extracted_audio_path = "sounds/extracted_audio.mp3"
shifted_audio_path = 'sounds/shifted_audio.wav'

video_source.audio.write_audiofile(extracted_audio_path)


def change_pitch(audio_path, output_path, pitch_factor):
    # Load audio
    y, sr = librosa.load(audio_path, sr=None)
    
    # Change pitch
    y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=pitch_factor)
    
    # Save shifted audio
    sf.write(output_path, y_shifted, sr)



# Change pitch of the audio
change_pitch(extracted_audio_path, shifted_audio_path, pitch_factor=-2) # Negative for lower pitch

# Combine with video
video_clip = VideoFileClip(f"{output_video_file_name}.mp4")

# second_clip = VideoFileClip(video_path)

audio_clip = AudioFileClip(shifted_audio_path)
final_video = video_clip.set_audio(audio_clip)
final_video.write_videofile('output/final_output_with_baritone_audio_v3_3.mp4', fps=video_clip.fps)