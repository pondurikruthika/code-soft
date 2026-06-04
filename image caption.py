from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Dense, Embedding, LSTM, Dropout, add
import numpy as np


base_model = VGG16()
feature_extractor = Model(
    inputs=base_model.inputs,
    outputs=base_model.layers[-2].output
)


def extract_features(filename):
    image = load_img(filename, target_size=(224,224))
    image = img_to_array(image)
    image = image.reshape((1,224,224,3))
    image = preprocess_input(image)
    feature = feature_extractor.predict(image, verbose=0)
    return feature


def load_captions(filename):
    captions = {}
    with open(filename, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            image_id = tokens[0]
            caption = ' '.join(tokens[1:])
            if image_id not in captions:
                captions[image_id] = []
            captions[image_id].append(caption)
    return captions


captions = load_captions("captions.txt")


all_captions = []
for cap_list in captions.values():
    all_captions.extend(cap_list)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_captions)

vocab_size = len(tokenizer.word_index) + 1
max_length = 34


inputs1 = Input(shape=(4096,))
fe1 = Dropout(0.5)(inputs1)
fe2 = Dense(256, activation='relu')(fe1)

inputs2 = Input(shape=(max_length,))
se1 = Embedding(vocab_size, 256, mask_zero=True)(inputs2)
se2 = Dropout(0.5)(se1)
se3 = LSTM(256)(se2)

decoder1 = add([fe2, se3])
decoder2 = Dense(256, activation='relu')(decoder1)
outputs = Dense(vocab_size, activation='softmax')(decoder2)

model = Model(inputs=[inputs1, inputs2], outputs=outputs)

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam'
)

print(model.summary())


def generate_caption(model, tokenizer, photo, max_length):
    text = "startseq"

    for i in range(max_length):

        sequence = tokenizer.texts_to_sequences([text])[0]
        sequence = pad_sequences(
            [sequence],
            maxlen=max_length
        )

        yhat = model.predict(
            [photo, sequence],
            verbose=0
        )

        yhat = np.argmax(yhat)

        word = tokenizer.index_word.get(yhat)

        if word is None:
            break

        text += " " + word

        if word == "endseq":
            break

    return text


image_path = "dog.jpg"

photo = extract_features(image_path)

caption = generate_caption(
    model,
    tokenizer,
    photo,
    max_length
)

print("Generated Caption:")
print(caption)
