if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import Python libraries
import threading
    
# import rcpy libraries
import rcpy 
import rcpy.button as button
import rcpy.led as led

# configure LEDs
rates = (1, 5, 10)
index = 0

# start leds
red = led.blink(led.RED, rates[index % len(rates)], led.ON)
green = led.blink(led.RED, rates[index % len(rates)], led.OFF)
blinking = True

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# function to step rate
def step():
    while rcpy.get_state() != rcpy.EXITING:
        if button.pressed(button.MODE):
            print("<MODE> pressed, stepping blinking rate")
            # increment rate
            index += 1
            red.set_rate(rates[index % len(rates)])
            green.set_rate(rates[index % len(rates)])

# run step function on a thread
step_thread = threading.Thread(target=step)
step_thread.start()

# welcome message
print("Green and red LEDs should be flashing")
print("Press button <MODE> to change the blink rate")
print("Press button <PAUSE> to stop or restart blinking")
print("Hold button <PAUSE> for 1.5 s to exit")

try:
    
    while rcpy.get_state() != rcpy.EXITING:

        print("Waiting for <PAUSE> button...")
        # this is a blocking call!
        if button.pressed(button.PAUSE, 2):

            # pause pressed
            print("<PAUSE> pressed")

            # this is a blocking call with a timeout!
            if button.released(button.PAUSE, 1.5):
                # released too soon!

                # toggle start
                if blinking:
                    print("Stopped blinking")
                    # stop leds
                    red.stop()
                    green.stop()
                    blinking = False

                else:
                    print("Started blinking")
                    # start leds
                    red = led.blink(led.RED, rates[index % len(rates)], led.ON)
                    green = led.blink(led.RED, rates[index % len(rates)], led.OFF)
                    blinking = True

            else:
                # timeout or did not release
                print("<PAUSE> held, exiting...")
                # exit
                break

except KeyboardInterrupt:
    # Catch Ctrl-C
    rcpy.set_state(rcpy.EXITING)
        
finally:

    print("Exiting...")

    # wait for step_thread to end
    step_thread.join()
    
    # say bye
    print("\nBye Beaglebone!")
            