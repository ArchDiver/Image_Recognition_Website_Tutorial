from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

X = 'cat'
Y = 'dog'

sample_Y_image = 'train/Y/images (49).jpg'

# Create a function that will tweak our images to prevent overfitting

datagen = ImageDataGenerator(
            rotation_range=40,
            width_shift_range = 0.2,
            height_shift_range= 0.2,
            rescale = 1.0/255,
            shear_range = 0.2, 
            zoom_range = 0.2,
            horizontal_flip = True,
            fill_mode = 'nearest')

img = load_img(sample_Y_image)

x = img_to_array(img)
x = x.reshape((1,) + x.shape)

i = 0

for batch in datagen.flow(X,
                batch_size = 1,
                save_to_dir= "preview",
                save_prefix= Y,
                save_format='jpeg'
                ):
  i += 1
  if i > 20:
    break
