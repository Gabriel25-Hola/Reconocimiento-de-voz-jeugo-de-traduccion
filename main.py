import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import deepl
import random
import time


#variables________________________
duration = 5
sample_rate = 44100
print("puedes comenzar a hablar")
puntaje = 0
errores = 0
max_errores = 5

palabras_por_niveles = {
    "facil":["gato", "perro", "manzana", "leche", "sol"],
    "medio":["platano", "amigo", "ventana", "amarillo"],
    "dificil":["tecnologia", "universidad", "informacion", "pronunciacion", "imaginacion"]
}
#____________________________________

print("Bienvenido al juego.")
print("Vas a ver una palabra en español, debes decirla en ingles, si esta bien ganaras 1 punto")

time.sleep(1)

nivel = input("En que nivel te gustaria jugar: facil, medio, dificil")

while nivel not in palabras_por_niveles:
    print("Nivel no encontrado, intenta otra vez")
    nivel = input("En que nivel te gustaria jugar: facil, medio, dificil")

word_list = palabras_por_niveles[nivel]
random.shuffle(word_list)

print("Vas a jugar el nivel", nivel)

recognizer = sr.Recognizer()

recognizer = sr.Recognizer()

for word in word_list:
    print("Debes de decir en ingles:", word)
    print("Puedes comenzar a hablar...")
    recording = sd.rec(int(duration * sample_rate), samplerate = sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("resultado.wav", sample_rate, recording)
    print("Grabacion completa, vamos a reconocer lo que dices")

    try:
        with sr.AudioFile("resultado.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language = "ES")
            client = deepl.DeepLClient("35870bce-545f-4ac7-9aca-258b24149803:fx")
            result = client.translate_text(word, target_lang="EN-US")

            if result.text == text:
                puntaje += 1
                print("Has dicho la palabra bien, te has ganado 1 punto")
            else:
                errores += 1
                print("No lo has dicho bien, debias decir:", result.text)
                print(f"Llevas {errores} de {max_errores}")
                if errores >= max_errores:
                    print("Juego Terminado, has cometido 5 errores")
                    break
    except sr.UnknownValueError:
        print("No te reconocimos lo que dijiste!")
print("Felcidades has obtenido", puntaje,"puntos")
