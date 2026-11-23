"""Beat placement for Chapter 6, Automated and Emerging Technologies.

Run from the repo root:

    python build/beats_ch06.py

The audio the pipeline reads is made from the upload by two commands.
The recorder was running for seven seconds before the lecture started and
for thirteen after it ended:

    ffmpeg -ss 7.3 -to 1407.5 -i audio/CH06-automation-raw.m4a \\
        -c:a aac -b:a 96k audio/CH06-automation.m4a

Then one cut inside the lecture. At 928.3 the machine-learning section
begins, and forty seconds in it is interrupted -- "Let's give you one
second, kids", a pause, then "Okay, machine learning take two", and the
section starts again from its first sentence. The cut removes the first
attempt and the interruption together, 69.8 seconds, and keeps take two
whole:

    ffmpeg -i audio/CH06-automation.m4a -filter_complex \\
        "[0:a]atrim=0:928.30,asetpts=N/SR/TB[a];\\
         [0:a]atrim=998.10,asetpts=N/SR/TB[b];\\
         [a][b]concat=n=2:v=0:a=1[out]" -map "[out]" \\
        -c:a aac -b:a 96k audio/CH06-automation-cut.m4a

Both cuts land in silence between sentences, and the join reads
"... does not replace every part of human expertise. Machine learning is
another approach to artificial intelligence."

This is the one edit of its kind in the course so far. Chapter 4's
restarted sentence was left exactly as delivered, because a stumble is
part of a delivery. A named retake with fifty seconds of room noise in
the middle of it is not: there is no reading of it that belongs in a
finished lesson, and the words that survive are the same words.

    python build/transcribe.py audio/CH06-automation-raw.m4a \\
        --model small --language en

Transcribed before either edit, then every timestamp shifted: minus 7.3
for the trim, and minus a further 69.8 for the words after the cut, with
the words inside it dropped. That is exact rather than a shortcut --
trimmed audio is the same samples moved along the clock -- and it saves
re-running the model on the same twenty-three minutes.

``build/repair_loops.find_loops`` reports no loops at all.

Anchors are copied from the transcript as it came out, mis-hearings and
all, never from the written script. "export systems" is expert systems,
"a physical such as temperature" has lost the word property, "immunity"
is humidity, "a pump or wall" is a valve, "jams" are arms, "end -roll
base" is the rule base, "facts applied by the user" is supplied, "a next
system" is an expert system, "of pure quality" is poor, "uses centers to
collect data" is sensors, and "Its results can be reusable" is
unreliable. A phrase corrected to the script would not be in the audio,
and would either fail to match or -- far worse -- match somewhere else.

Several anchors repeat earlier wording almost exactly: the greenhouse is
worked twice, once to introduce the three parts and once to close the
chapter, and the four expert-system components are named twice. Matching
runs forward from the previous beat, so the second pass finds the second
occurrence. Any anchor that resolved out of order would fail loudly
rather than quietly marking the wrong sentence.
"""

from mkbeats import build

BEATS = [
    # ------------------------------------------------------- 0. opening
    ("open", "Alright guys, welcome to Chapter 6 of Cambridge"),
    ("three_areas", "In this lesson, we'll explore three connected areas"),
    ("sensors_actuators", "We'll see how sensors, processors, and actuators "
                          "work together"),
    ("robots_where", "where robots are used and how export systems"),
    ("focus_on", "focus on how each system receives information"),
    ("produces", "processes it, and produces an action of results"),

    # --------------------------------------- 1. what an automated system is
    ("auto_open", "So an automated system carries out a process with limited"),
    ("follow_info", "A simple way to understand one is to follow the "
                    "information through the system"),
    ("sensor_gathers", "A sensor gathers data from the environment"),
    ("micro_receives", "A microprocessor receives and processes that data"),
    ("actuator_does", "An actuator then produces a physical action as a "
                      "change"),
    ("greenhouse", "You know, consider an automated greenhouse"),
    ("moisture", "A moisture sensor measures the water level in the soil"),
    ("reading_sent", "A reading is sent to the microprocessor"),
    ("compares", "The microprocessor compares it with a desired moisture "
                 "level"),
    ("too_dry", "If the soil is too dry, the control program sends a signal"),
    ("opens_valve", "The actuator opens a water valve or it starts to pump"),
    ("another_reading", "So the sensor then takes another reading"),
    ("check_result", "the system can check whether its action has actually "
                     "produced a required result"),
    ("still_dry", "If the soil is still too dry, the system can continue "
                  "watering"),
    ("target_reached", "When the target level is reached, it can stop"),
    ("feedback_named", "This repeated measurement and adjustment is called "
                       "the feedback control"),

    # ------------------------------------------------- 2. the feedback loop
    ("loop_open", "What is a feedback control?"),
    ("measures_property", "First, a sensor measures a physical such as "
                          "temperature, light, pressure or moisture"),
    ("sends_reading", "The sensor sends it's reading to the control system"),
    ("converted", "The reading may need to be converted into digital data"),
    ("compare_preset", "The microprocessor compares the reading with a "
                       "preset or desired value"),
    ("decides", "So the control program decides whether the action is "
                "needed"),
    ("signal_actuator", "the microprocessor sends a signal to an actuator"),
    ("changes_system", "The actuator changes the physical system"),
    ("measures_again", "Then the sensor measures the result again and the "
                       "cycle repeats"),
    ("heating", "For example, in a heating system"),
    ("room_temp", "The microprocessor compares the room temperature with "
                  "the temperature selected by the user"),
    ("too_cold", "If the room temperature is too cold"),
    ("switch_off", "the system can switch the heater off"),
    ("essential", "The new sensor reading is essential"),
    ("without_feedback", "Without feedback, the system may keep heating"),
    ("oven", "Your room will turn into an oven"),
    ("exam_cycle", "So in an exam answer, explain the complete cycle"),
    ("five_words", "Sensor, processing, decision actuator, and the new "
                   "sensor reading"),

    # -------------------------------------------- 3. where automation is used
    ("uses_open", "automated systems are used in many settings"),
    ("lighting", "An automatic lighting system uses a light sensor"),
    ("proximity", "Or proximity to sensor"),
    ("walking_near", "when you're walking near close by, the light turns on"),
    ("lamp_output", "Its output could be a signal that switches a lamp on "
                    "or off"),
    ("weather", "A weather station might use sensors to measure temperature, "
                "pressure, immunity"),
    ("record_alarm", "It can process and record readings, display them, or "
                     "send an alarm"),
    ("tank", "A control system can then operate a pump or wall"),
    ("vehicle", "or sensors measure speed, proximity, and acceleration"),
    ("warning_brake", "The system uses these readings to provide a warning "
                      "or activate a braking system"),
    ("dashboard", "When you see a red light and your dashboard"),
    ("identify_three", "In each example, you should identify what that "
                       "sensor measures"),
    ("structure", "That gives you a clear structure for explaining how an "
                  "automated system works"),

    # ----------------------------------------------- 4. weighing automation
    ("weigh_open", "So automation has advantages"),
    ("continuous", "Automated systems can work, you know, continuously and "
                   "perform the same task consistently"),
    ("quick_precise", "They can respond quickly to sensor reading and carry "
                      "out precise repeated actions"),
    ("dangerous_places", "They can also operate in dangerous places where it "
                         "may be unsafe"),
    ("record_data", "Some systems can automatically record data in helping "
                    "people monitor changes"),
    ("costs_open", "But automation also creates some risk and cost"),
    ("expensive", "So equipment can be expensive to purchase or to produce, "
                  "install, program and maintain"),
    ("wrong_action", "If a sensor gives an incorrect reading or the software "
                     "makes a poor decision"),
    ("dangerous_where", "That can be dangerous in a heating system, even in "
                        "cars"),
    ("unexpected", "So an automated system may also struggle when something "
                   "unexpected happens"),
    ("jobs", "automation can reduce the need for some jobs"),
    ("cyber", "So connected systems can also create cybersecurity or "
              "privacy risk"),
    ("not_good_bad", "do not simply say it is a good or bad"),
    ("connect_situation", "Connect each advantage or disadvantage to the "
                          "situation in the question"),

    # ---------------------------------------------- 5. what makes a robot
    ("robot_open", "All right, now talk about robotics"),
    ("robotics_is", "Robotics is the branch of computer science which "
                    "concerns itself with designing"),
    ("robot_is", "So a robot is a programmable and normally combines a "
                 "mechanical structure with electrical components"),
    ("structure_parts", "The mechanical structure includes a frame, joint, "
                        "wheels, or jams"),
    ("robot_sensors", "And sensors collect information about the robot or "
                      "its environment"),
    ("robot_processor", "A microprocessor or a controller runs a program "
                        "that controls the robot"),
    ("robot_actuator", "Actuator again produces movement or another physical "
                       "action"),
    ("programmable", "So the robot is programmable"),
    ("distinguish", "These characteristics distinguish a robot from an "
                    "ordinary machine"),
    ("washing_machine", "For example, a washing machine, it's automated"),
    ("not_a_robot", "but it does not necessarily have the mechanical "
                    "structure and programmable control"),
    ("checklist", "So when asked whether something is a robot, look for a "
                  "mechanical structure"),

    # ------------------------------------------------ 6. where robots work
    ("robot_uses_open", "Robots are used in many different areas"),
    ("industry", "In industry, robots can assemble products, weld components"),
    ("precise_moves", "They can repeat precise movements and working "
                      "environments"),
    ("transport", "So in transport or warehouse, robotic vehicles move goods"),
    ("drones", "Drones can be used for delivery or monitoring"),
    ("agriculture", "In agriculture, robots can help with harvesting"),
    ("large_areas", "This can cover large areas and reduce people's exposure "
                    "to chemical"),
    ("medicine", "In medicine, robots can assist with controlled movements "
                 "during a surgery"),
    ("homes", "In homes or robot, my vacuum floors"),
    ("entertainment", "Robots can also be used to entertain for competitions"),
    ("depends", "The best example depends on the scenario"),
    ("factory_answer", "If a question describes a dangerous factory"),
    ("limitations", "Then consider limitations"),
    ("balanced", "A balanced evaluation considers both benefits and "
                 "limitations"),

    # ------------------------------------------- 7. artificial intelligence
    ("ai_open", "Artificial intelligence, we usually call it AI"),
    ("ai_is", "is the branch of computer science which concerns itself with "
              "simulating intelligent behavior"),
    ("ai_uses", "An AI system uses data and rules to process both inputs"),
    ("ai_reasons", "It can reason about the information it receives"),
    ("mistake", "a common mistake is to define AI only as a computer thing"),
    ("too_vague", "That description is too vague for a strong"),
    ("instead", "Instead, explain that an AI system uses data and rules to "
                "process information"),
    ("can_learn", "Some systems can also learn from examples and adapt their "
                  "processes"),
    ("two_examples", "two examples, you know, we'll examine one expert "
                     "system"),

    # ---------------------------------------------------- 8. expert systems
    ("expert_open", "so an expert system uses stored knowledge and rules of "
                    "rules to provide advice"),
    ("plant_disease", "an expert system might help identify a plant disease"),
    ("four_parts", "An expert system usually has four components"),
    ("knowledge_base", "The knowledge base, which stores the facts and "
                       "specialist knowledge"),
    ("rule_base", "The rule base stores logical rules that connect facts to "
                  "conclusions"),
    ("inference", "Then you have the inference engine which applies through "
                  "the rules"),
    ("interface", "And the user interface collects information and presents "
                  "questions, advice or explanations"),
    ("follow_open", "So let's follow how an expert system works"),
    ("user_enters", "The user enters facts or answers questions through the "
                    "interface"),
    ("engine_checks", "The inference engine checks the facts against the "
                      "knowledge base and end -roll base"),
    ("applies_rules", "The inference engine then applies those rules to the "
                      "stored knowledge and facts supplied by the user"),
    ("presents", "The user interface collects information and presents "
                 "questions, right?"),
    ("displays", "finally, the interface displays the result and explains "
                 "how to reach that conclusion"),
    ("engine_role", "The inference engine, once again, is part that applies "
                    "the rules"),
    ("kb_role", "The knowledge base contains the facts"),
    ("rb_role", "The rule base contains the logic"),
    ("ui_role", "The user interface allows the person to interact with the "
                "system"),
    ("distinct", "So keep these roles distinct in your answer"),
    ("strengths_open", "So, expert systems have, you know, strength and "
                       "limited"),
    ("consistent", "They can apply stored rule consistently"),
    ("available", "They are available whenever a user needs them"),
    ("preserve", "They can also preserve the specialist knowledge and make "
                 "it available"),
    ("explain_rules", "Some expert systems can explain their conclusion by "
                      "showing which rules were applied"),
    ("depends_quality", "However, the quality of these advice depends on the "
                        "knowledge and rules"),
    ("out_of_date", "If the knowledge base is incomplete or out of date"),
    ("not_covered", "So expert systems may struggle with cases that are not "
                    "covered by their roles"),
    ("no_empathy", "They also lack human empathy, judgment and "
                   "accountability"),
    ("updating", "So updating the knowledge base can take time"),
    ("narrow_area", "So a next system can be useful in a narrow area"),

    # --------------------------------------------------- 9. machine learning
    ("ml_open", "Machine learning is another approach to artificial "
                "intelligence"),
    ("finds_patterns", "A machine learning system uses examples and data to "
                       "find patterns"),
    ("during_training", "during training and algorithm processes data and "
                        "adjusts an internal model"),
    ("predictions", "That model is then used to make predictions or "
                    "classifications"),
    ("leaves", "a system could be trained using many labeled images of "
               "healthy and unhealthy plant leaves"),
    ("distinguishes", "The model tries to identify patterns that "
                      "distinguishes two groups"),
    ("new_image", "Once trained, it can examine a new image and predict "
                  "which group it belongs to"),
    ("stages_open", "So a basic machine learning path process has several "
                    "stages"),
    ("collect", "First, collect suitable data"),
    ("prepare", "Next, prepare the data and label it if necessary"),
    ("train", "Then train an algorithm to identify patterns"),
    ("evaluate", "After training, evaluate the model using data that was not "
                 "used to train it"),
    ("handle_new", "This helps check whether it can actually handle new "
                   "examples"),
    ("use_model", "The model can then be used to process new inputs"),
    ("monitor", "Its errors should be monitored too"),
    ("update", "And the model or training data may need to be updated on a "
               "regular basis"),
    ("no_guarantee", "So machine learning does not guarantee that every "
                     "prediction is correct"),
    ("biased", "If the training data is incomplete, biased, or of pure "
               "quality"),
    ("quality_matters", "So the quality of data matters the most"),

    # ------------------------------------------------- 10. the comparison
    ("compare_open", "So let's compare an expert system with machine "
                     "learning"),
    ("es_facts", "An expert system uses facts and and rules supplied by "
                 "experts"),
    ("ml_patterns", "Machine learning identifies patterns in training data"),
    ("es_traced", "The reasoning of an expert system often can be traced to "
                  "the rules"),
    ("ml_harder", "The decisions of machine learning models may be harder to "
                  "explain"),
    ("es_static", "An expert system does not automatically change its rules "
                  "unless someone updates it"),
    ("ml_adapts", "A machine learning model may adapt when it is retrained"),
    ("es_narrow", "Expert systems can work well in narrow areas where the "
                  "knowledge and rules are clear"),
    ("store_example", "if you're building something from the knowledge base "
                      "of a store"),
    ("ml_large", "But machine learning works well when there are patterns to "
                 "learn from a large set of examples"),
    ("neither", "So neither situation is suitable for every problem"),
    ("explain_how", "So when comparing them, explain how each system "
                    "produces these results"),

    # ---------------------------------------------------- 11. one example
    ("example_open", "Let's look at an example, right? Again, of the "
                     "greenhouse"),
    ("ex_sensor", "A moisture sensor measures the water level in the soil"),
    ("ex_sends", "The sensor sends the reading to a microprocessor"),
    ("ex_compares", "The microprocessor compares the reading with the "
                    "required at moisture level"),
    ("ex_below", "If the reading is below the target, the control program "
                 "activates or an actuator"),
    ("ex_valve", "The actuator opens a water wall"),
    ("ex_again", "The sensor measures the soil again, which allows the "
                 "system to check"),
    ("ex_that_is", "That is the automated control"),
    ("ex_robot", "A robot might be used to move through a greenhouse"),
    ("ex_robot_parts", "It could also use sensors to collect readings, a "
                       "processor to run its program"),
    ("ex_ai", "An artificial intelligence system could analyze the collected "
              "readings"),
    ("ex_expert", "A rule -based expert system, you know, might use the "
                  "stored rules"),
    ("ex_ml", "A machine learning model might use previous data to predict"),
    ("ex_depends", "These systems can support decisions, but their results "
                   "will depend on reliable sensors"),

    # ---------------------------------------------------------- 12. recap
    ("recap_open", "So, to summarize, an automated system uses centers to "
                   "collect data"),
    ("r_processor", "a processor to make decisions, and an actuator to "
                    "change their environment"),
    ("r_loop", "In a feedback loop, the system measures again after the "
               "action"),
    ("r_benefits", "Automation improves speed, consistency, and safety"),
    ("r_costs", "but it can also be costly and may fail or behave poorly"),
    ("r_robot", "A robot is programmable and combines a mechanical structure "
                "with electrical control components"),
    ("r_robot_parts", "such as sensor, a processor, and actuator"),
    ("r_ai", "Artificial intelligence uses data and rules to process inputs "
             "and produce conclusions or actions"),
    ("r_adapt", "It may also learn and adapt"),
    ("r_expert", "So an expert system uses a knowledge base, a rule base"),
    ("r_engine", "An inference engine and a user interface"),
    ("r_ml", "Machine learning trains a model to identify patterns in data"),
    ("r_unreliable", "Its results can be reusable right if the data is poor "
                     "or biased"),
    ("exam_order", "So when answering exam questions describe the process in "
                   "order"),
    ("evaluations", "For evaluations right use details from the scenario"),
    ("close", "This brings us to the end of chapter 6 automated and emerging "
              "technologies"),
    ("questions", "if you're following the book, let's do all the questions"),
]

if __name__ == "__main__":
    build("CH06-automation", "cs.automation", BEATS, "CH06-automation",
          "Cambridge O Level 2210 Chapter 6: Automated and Emerging "
          "Technologies. Anchors copied from the transcript, mis-hearings "
          "and all.")
