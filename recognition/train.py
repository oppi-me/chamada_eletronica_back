import math
import os
import pickle

import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
from sklearn import neighbors


def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    x = []
    y = []

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print('Imagem {} não adequada para o treinamento: {}'
                          .format(img_path,
                                  'Nenhum rosto foi encontrado.' if len(face_bounding_boxes) < 1
                                  else "Mais de um rosto foi encontrado."))
            else:
                # Add face encoding for current image to the training set
                x.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Determine how many neighbors to use for weighting in the KNN classifier
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(x))))
        if verbose:
            print("n_neighbors foi gerado automaticamente:", n_neighbors)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(x, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


if __name__ == "__main__":
    print("Treinando classificador KNN...")
    train("../static", model_save_path="../../static/trained_knn_model.clf", n_neighbors=1)
    print("Treinamento Completo!")
