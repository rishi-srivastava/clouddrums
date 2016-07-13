
from django.shortcuts import render
import random
import time
import subprocess

# kick
kick1 = "/home/rishisriv/Sounds/HipHopKit/HipHopKick.wav"
kick2 = "/home/rishisriv/Sounds/RockKit/RockKick2.wav"
kick3 = "/home/rishisriv/Sounds/BongosKit/BongoLow.wav"

# snare
snare1 = "/home/rishisriv/Sounds/HipHopKit/HipHopSnare.wav"
snare2 = "/home/rishisriv/Sounds/RockKit/RockSnare.wav"
snare3 = "/home/rishisriv/Sounds/BongosKit/BongoMid.wav"

# hiHat and ride
hiHat1 = "/home/rishisriv/Sounds/HipHopKit/HipHopHat.wav"
hiHat2 = "/home/rishisriv/Sounds/RockKit/RockHat2.wav"
hiHat3 = "/home/rishisriv/Sounds/BongosKit/BongoHigh.wav"
ride = "/home/rishisriv/Sounds/RockKit/RockRide2.wav"


def hitOrNo(n):
    i = random.randrange(0, 9)
    if (i < n):
        return 1
    else:
        return 0


def createForm(request):

    return render(request, 'form.html')


def playOnce (beat, num16ths, valid, kick, snare, hiHat, kickPath, snarePath, hiHatPath, wholeBeat, beatTime):
    while (beat <= (num16ths + 1) and valid == 1):
        kickPlay = 0
        if (beat == (num16ths + 1)):
            break

        # play kick
        if (kick[beat - 1] == 1):
            kickPlay = 1
            return_code = subprocess.Popen(["afplay", kickPath])

        # play snare
        if (snare[beat - 1] == 1 and kickPlay == 0):
            # print("snare ", end="")
            return_code = subprocess.Popen(["afplay", snarePath])

        # play hiHat
        if (hiHat[beat - 1] == 1):
            return_code = subprocess.Popen(["afplay", hiHatPath])

        if (beat % 4 == 0):
            wholeBeat += 1

        time.sleep(beatTime)  # wait beatTime seconds for next beat
        beat += 1


def printBPM(request):
    if ('q' in request.GET and 'p' in request.GET and "Kit" in request.GET):
        for key, value in request.GET.items():
            print(key, value)

        # choose loop length

        loopLength = int(request.GET['p'])
        num16ths = loopLength * 16

        kick = [None] * num16ths
        snare = [None] * num16ths
        hiHat = [None] * num16ths
        beat = 1

        # generate piano roll
        while (beat <= num16ths):
            # kick
            if (beat % 4 == 0 or (beat - 2) % 4 == 0):
                kick[beat - 1] = hitOrNo(2)
            if ((beat + 1) % 4 == 0):
                kick[beat - 1] = hitOrNo(3)
            if ((beat - 1) % 4 == 0):
                kick[beat - 1] = hitOrNo(1)
            if ((beat - 1) % 8 == 0):
                kick[beat - 1] = 1
            # snare
            if ((beat - 1) % 8 == 0):
                snare[beat - 1] = hitOrNo(1)
            if (beat % 2 == 0 or (beat + 1) % 4 == 0):
                snare[beat - 1] = hitOrNo(2)
            if ((beat + 3) % 8 == 0):
                snare[beat - 1] = hitOrNo(10)

            # hiHat
            if ((beat - 1) % 2 == 0):
                hiHat[beat - 1] = hitOrNo(10)
            if ((beat + 2) % 4 == 0):
                hiHat[beat - 1] = hitOrNo(3)
            if (beat % 4 == 0):
                hiHat[beat - 1] = hitOrNo(2)

            beat += 1

        # get user input

        kit = str(request.GET['Kit'])

        if (kit == 'HipHop'):  # hip hop kit
            kickPath = str(kick1)
            snarePath = str(snare1)
            hiHatPath = str(hiHat1)

        if (kit == 'Rock'):  # rock kit
            kickPath = str(kick2)
            snarePath = str(snare2)
            # choose hi hat or ride beat
            rideOrHat = hitOrNo(5)  # int(rideOrHat) RIDE OR HAT IS NOW RANDOM -> FIX IN FUTURE????
            if (rideOrHat == 1):
                hiHatPath = str(hiHat2)
            if (rideOrHat == 0):
                hiHatPath = str(ride)

        if (kit == 'Bongos'):  # bongo kit
            kickPath = str(kick3)
            snarePath = str(snare3)
            hiHatPath = str(hiHat3)

        bpm = float(request.GET['q'])

        beatTime = 15 / bpm  # time in seconds between beats

        if request.GET['Play'] == 'Play':
            global valid
            print ("a")
            valid = 1
            abc = request.GET['Play']
            print (abc)
        if request.GET['Play'] == 'Stop':
            global valid
            valid = 0
            time.sleep(100000)
            abc = request.GET['Play']
            print (abc)

        while (valid == 1):
            beat = 1
            wholeBeat = 1

            if request.GET['Play'] == 'Stop':
                valid = 0
                time.sleep(100000)
                abc = request.GET['Play']
                print (abc)

            while (beat <= (num16ths + 1) and valid == 1):
                kickPlay = 0
                if (beat == (num16ths + 1)):
                    break

                if request.GET['Play'] == 'Stop':
                    valid = 0
                    time.sleep(100000)
                    abc = request.GET['Play']
                    print (abc)

                if (kick[beat - 1] == 1):
                    kickPlay = 1
                    return_code = subprocess.Popen(["afplay", kickPath])

                # play snare
                if (snare[beat - 1] == 1 and kickPlay == 0):
                    # print("snare ", end="")
                    return_code = subprocess.Popen(["afplay", snarePath])

                # play hiHat
                if (hiHat[beat - 1] == 1):
                    return_code = subprocess.Popen(["afplay", hiHatPath])

                if (beat % 4 == 0):
                    wholeBeat += 1

                time.sleep(beatTime)  # wait beatTime seconds for next beat
                beat += 1

    else:
        return render(request, 'form.html')

    return render(request, 'form.html')


def about(request):

    return render(request, 'about.html')
