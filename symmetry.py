import os
import random
import time

from psychopy import core
from Template_Task_Psychopy.task_template import TaskTemplate
from list_images import images


class Symmetry(TaskTemplate):
    # IMPORTANT ! To MODIFY IF NEEDED
    nb_ans = 2
    response_pad = True  # has to be set on "True" on production.
    eye_tracker_study = True
    # END OF IMPORTANT
    trials = 100
    score = 0
    yes_key_name = "verte"
    yes_key_code = "6"
    no_key_name = "rouge"
    no_key_code = "0"
    quit_code = "3"
    keys = ["space", yes_key_code, no_key_code, quit_code]
    launch_example = True
    exp_start_timestamp = time.time()

    next = f"Pour passer à l'instruction suivante, appuyez sur la touche {yes_key_name}"

    instructions = [
        f"Dans cette expérience : \n\n - appuyez sur la touche {yes_key_name} pour répondre oui ou pour "
        f"selectionner la réponse de droite. \n\n - appuyez sur la touche {no_key_name} pour répondre non ou pour "
        f"selectionner la réponse de gauche.", "N'appuyez sur les touches colorées que lorsque la question apparaît.",

        f"Placez vos index sur les touches {no_key_name} et {yes_key_name}."]

    csv_headers = ['id_candidate', 'no_trial', 'ans_candidate',
                   'good_ans', 'result', 'score', 'reaction_time', 'time_stamp']

    def task(self, no_trial):
        self.create_visual_image(image=f'img/{images[no_trial]}',
                                 size=(1512, 982)).draw()
        self.win.flip()
        core.wait(2)
        self.create_visual_text("Les deux barres sont-elles parallèles ? \n\n Non / Oui").draw()
        self.win.flip()
        time_stamp = time.time() - self.response_pad_timestamp
        resp, rt = self.get_response_with_time()
        good_ans = [self.yes_key_code if int(images[no_trial][images[no_trial].find("_") + 1:images[no_trial].find(".")]) >= 25 and
                    int(images[no_trial][images[no_trial].find("_") + 1:images[no_trial].find(".")]) != 102 else self.no_key_code][0]
        if resp == good_ans and no_trial < 100:
            self.score += 1

        if self.response_pad:
            self.update_csv(self.participant, no_trial, resp, good_ans, int(resp == good_ans), self.score,
                            round(rt - time_stamp, 2), round(rt, 2))
        else:
            self.update_csv(self.participant, no_trial, resp, good_ans, int(resp == good_ans), self.score, round(rt, 2),
                            round(time.time() - self.exp_start_timestamp, 2))
        if self.launch_example:
            return resp == good_ans

    def example(self):
        score_example = 0
        example = self.create_visual_text(text="Commençons par un petit entraînement")
        tutoriel_end = self.create_visual_text(
            text="L'entraînement est désormais terminé"
        )
        example.draw()
        self.create_visual_text(self.next, pos=(0, -0.4), font_size=0.04).draw()
        self.win.flip()
        self.wait_yes(self.yes_key_code)
        for u in range(100, 103):
            if self.task(u):
                score_example += 1
                self.create_visual_text(
                    f"Bravo ! Vous avez {score_example}/{u - 99}"
                ).draw()
                self.win.flip()
                core.wait(2)
            else:
                self.create_visual_text(
                    f"Dommage... Vous avez {score_example}/{u - 99}"
                ).draw()
                self.win.flip()
                core.wait(2)
        self.create_visual_text(f"Vous avez obtenu {score_example}/3").draw()
        self.win.flip()
        core.wait(5)
        tutoriel_end.draw()
        self.win.flip()
        core.wait(5)


exp = Symmetry("csv")
exp.start()
