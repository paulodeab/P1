#LECUN - CNN => Josh Starmer
# Livro : https://d2l.ai/index.html - Dive into Deep Learning
import cv2
import mediapipe as mp
import time
from sender import ModBusSender

class RecognitionHand():

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        
        # self._modbus = ModBusSender('127.0.0.1', 502, 1)
        # self._modbus.get_connection()
    
    def recoginitionInitialize(self):
        cap = cv2.VideoCapture(0)
        detection_times = []

        with self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    continue

                # Início da medição do tempo para detecção
                start_time = time.time()

                # Inverte a imagem para visualização de selfie e converte BGR para RGB
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Definindo a linha de segurança a 3/4 da altura da imagem
                linha_y = int(image.shape[0] * 0.65)
                cv2.line(image, (0, linha_y), (image.shape[1], linha_y), (255, 0, 0), 2)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        try:
                            self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                            # Verificar cada ponto de referência dos dedos
                            for landmark in hand_landmarks.landmark:
                                count = 0
                                ponto_y = int(landmark.y * image.shape[0])
                                if ponto_y > linha_y:
                                    count += 1
                                    
                                    # self._modbus.send_signal(1)
                                    cv2.line(image, (0, linha_y), (image.shape[1], linha_y), (0, 0, 255), 2)
                                    print("Dedo passou da linha! ", count)

                                    # Captura o tempo de detecção
                                    detection_time = time.time() - start_time
                                    detection_times.append(detection_time)

                        except Exception as e:
                            print("Falha: ", e)

                # Exibe a imagem processada
                cv2.imshow('Hand Recognition', image)
                
                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()
        
        # Calcula a média de tempo de detecção
        if detection_times:
            avg_detection_time = sum(detection_times) / len(detection_times)
            print(f'Tempo médio de detecção da ultrapassagem da linha: {avg_detection_time:.4f} segundos')
        else:
            print('Nenhuma ultrapassagem de linha detectada.')

# Criação da instância e inicialização do reconhecimento
recognition_hand = RecognitionHand()
recognition_hand.recoginitionInitialize()





