import torch
import numpy as np
from torch.utils.data import DataLoader, Dataset
from PIL import Image
from torchvision import transforms, models

# Definir transformaciones
def get_transform():
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=3),  # Convertir a 3 canales
        transforms.Resize((224, 224)),  # Ajusta según el tamaño de entrada de tu modelo
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

# Clase para cargar datos desde un archivo CSV
class SignMNISTDataset(Dataset):
    def __init__(self, csv_file, transform=None):
        self.data = np.loadtxt(csv_file, delimiter=',', skiprows=1)  # Cargar datos CSV
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image = self.data[idx, 1:].reshape(28, 28)  # Ajusta según el formato del CSV
        label = int(self.data[idx, 0])
        image = Image.fromarray(image.astype(np.uint8), 'L')  # Convertir a imagen en escala de grises
        if self.transform:
            image = self.transform(image)
        return image, label

# Cargar datos de prueba
def get_test_loader(batch_size=32):
    transform = get_transform()  # Definir transformaciones aquí
    dataset = SignMNISTDataset(csv_file='Gestos/Data/sign_mnist_train.csv', transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)
    return dataloader

# Función para evaluar el modelo
def evaluate_model(model, dataloader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in dataloader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    return 100 * correct / total

# Cargar o definir el modelo
def load_model():
    model = models.resnet18(weights='DEFAULT')  # Usa la opción 'weights' en lugar de 'pretrained'
    model.fc = torch.nn.Linear(model.fc.in_features, 26)  # Ajustar el número de clases a 26
    
    try:
        state_dict = torch.load('Gestos/checkpoint.pth')
        
        # Comprobar si las dimensiones de la primera capa convolucional coinciden
        if state_dict['conv1.weight'].shape != model.conv1.weight.shape:
            print(f"Ajustando la capa conv1 del checkpoint de {state_dict['conv1.weight'].shape} a {model.conv1.weight.shape}")
            
            # Crear un nuevo tensor con las dimensiones correctas y copiar los datos antiguos
            new_conv1_weight = torch.zeros_like(model.conv1.weight)
            min_shape = (
                min(new_conv1_weight.shape[0], state_dict['conv1.weight'].shape[0]),
                min(new_conv1_weight.shape[1], state_dict['conv1.weight'].shape[1]),
                min(new_conv1_weight.shape[2], state_dict['conv1.weight'].shape[2]),
                min(new_conv1_weight.shape[3], state_dict['conv1.weight'].shape[3]),
            )
            new_conv1_weight[:min_shape[0], :min_shape[1], :min_shape[2], :min_shape[3]] = state_dict['conv1.weight'][:min_shape[0], :min_shape[1], :min_shape[2], :min_shape[3]]
            
            # Reemplazar los pesos en el state_dict
            state_dict['conv1.weight'] = new_conv1_weight
        
        model.load_state_dict(state_dict, strict=False)  # Cargar los pesos con el modelo
        model.eval()
        return model
    except FileNotFoundError as e:
        print(f"Error al cargar el modelo: {e}")
        raise

if __name__ == '__main__':
    test_loader = get_test_loader()
    model = load_model()
    accuracy = evaluate_model(model, test_loader)
    print(f'Accuracy: {accuracy:.2f}%')
