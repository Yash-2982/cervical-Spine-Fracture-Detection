import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense

# Define the model architecture
def create_model(input_shape):
    # Define input layer
    inputs = Input(shape=input_shape)

    # Convolutional layers
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    maxpool1 = MaxPooling2D((2, 2), padding='same')(conv1)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(maxpool1)
    maxpool2 = MaxPooling2D((2, 2), padding='same')(conv2)

    # Flatten layer
    flatten = Flatten()(maxpool2)

    # Dense layers
    dense1 = Dense(128, activation='relu')(flatten)
    outputs = Dense(10, activation='softmax')(dense1)  # Assuming 10 output classes

    # Define the model
    model = Model(inputs=inputs, outputs=outputs)
    
    return model

# Define input shape
input_shape = (28, 28, 1)  # Example input shape for MNIST data

# Create the model
model = create_model(input_shape)

# Print model summary
print("Model Summary:")
model.summary()

# Visualize model architecture
from tensorflow.keras.utils import plot_model
plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)
print("Model architecture visualized and saved as 'model_plot.png'.")

# Inspect individual layers
print("\nLayer Information:")
for layer in model.layers:
    print(layer.name, layer.trainable, layer.output_shape, layer.activation)

# Inspect layer configurations
print("\nLayer Configurations:")
for layer in model.layers:
    print(layer.get_config())
