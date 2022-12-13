# Imports
# from fhirpy import SyncFHIRClient
# from fhir.resources.patient import Patient
from fhir.resources.observation import Observation
# from fhir.resources.humanname import HumanName
# from fhir.resources.contactpoint import ContactPoint
# from fhir.resources.reference import Reference
# from fhir.resources.codeableconcept import CodeableConcept
# from fhir.resources.coding import Coding
# from fhir.resources.quantity import Quantity

import json
from datetime import datetime
from patient_registration import input_choice
from dataclasses import dataclass, InitVar


# lokalisation
def lokalisation_lunge() -> list[str]:
    lok = ["rechts", "links", "rechts basal", "links basal", "rechts apikal",
           "links apikal", "beidseits", "beidseits basal", "über dem Mittellappen"]
    return (lok)


def lokalisation_abdomen() -> list[str]:
    lok = ["generalisiert", "rechter unterer Quadrant", "rechter oberer Quadrant",
           "linker oberer Quadrant", "linker unterer Quadrant", "über McBurny", "über Lanz"]
    return (lok)


def list_int(r1: int, r2: int) -> list[int]:
    return list(range(r1, r2 + 1))


# input_and_choices
def input_choice_n(q: str, cho: list[str]) -> int:
    """ @param: question: str: the question
        @param: choices: list[str]: a list of strings. they are the possible choices in input
        returns integers annotatet to choices to a question, Enter is default and corresponds to 0 (first) element of the list 
    """
    choices = [":\n"]
    ns = []

    # annotate a number for each element of the list. "" corresponds to ENTER
    for n in range(len(cho)):
        if cho[n] == "":
            choices += ["\n ENTER = default \n"]
            ns += [str("")]
            n_enter = n
        else:
            choices += [f"{n} = {cho[n]} \n"]
            ns += [str(n)]

    ans_in = input(f"\n \n {q} {' '.join(choices)}: ")
    while ans_in not in ns:
        print("Invalid answer. Try again.")
        ans_in = input(f"\n \n {q} {''.join(choices)}: ")
    else:
        if ans_in == "":
            return (int(n_enter))
        else:
            return (int(ans_in))


def input_default(organ: str) -> bool:
    """
    @param organ: str
    input_default() returns True when no input Enter, else returns False
    """
    if input(f"{organ} [ENTER for no pathological oberservation, else any key]: ") == "":
        return True
    else:
        return False


def examinate_str(organ: str, values_default: dict, values_patho: dict) -> str:
    # accumulator for string output
    out = []

    # opb for the complete organ (no pathological observation)
    if input_default(organ):
        for value_name in values_default:
            value_block = f"{value_name}: {values_default[value_name]}; "
            out += [value_block]
        return (f"{organ}: {''.join(out)}")

    # pathological observation in organ
    else:
        for value_name in values_patho:
            # check for each value_name if default is wanted
            if (n_of_value := input_choice_n(value_name, values_patho[value_name])) == 0:
                # default observation
                value_block = f"{value_name}: {values_default[value_name]}; "
                out += [value_block]
            else:
                # patho observation
                value_block = f"{value_name}: {values_patho[value_name][n_of_value]}; "
                out += [value_block]
        return ((f"{organ}: {''.join(out)}"))

        # for value_name in values:
        #    if input_default(organ): # recursive function might be possibility or put chunk in function?
        #        new_value = input(f"{value_name}: ")
        #        value_block = f"{value_name}: {new_value}, "
        #        out += [value_block]
        # return (f"{organ}: {''.join(out)}")


if __name__ == "__main__":

    while input_choice("\n #### Welcome to a simple command-line questionaire for a physical obeservation of the heart, lung and abdomen. #### \npress ENTER to start: ", [""]) != "":
        print("invalid answer. Try again.")

    # author Michael Wegert
    # part 1 plain text output. no loinc or snomed ct codes
    # documentation from https://www.ukurs.uni-freiburg.de
    # Kopf_Hals

    # Herz
    dictionary_cor_default = {"Herztöne": "rein",
                              "Herzrhytmus": "rhytmisch",
                              "Herzgeräusche": "keine",
                              "Herzgeräusche_pm": "",
                              "Herzfrequenz": "normofrequent"
                              }

    dictionary_cor_patho = {"Herztöne": ["", "2.Herzton gespalten"],
                            "Herzrhytmus": ["", "rhytmisch", "arrythmisch"],
                            "Herzgeräusche": ["", "systolisch", "diastolisch", "systolisch-diastolisch"],
                            "Herzgeräusche_pm": ["", "2.ICR re parasternal", "2.ICR li parasternal", "5.ICR li mcl", "3.ICR li parasternal", "4.ICR re parasternal"],
                            "Herzfrequenz": ["", "tachykard", "bradykard"]
                            }

    c = examinate_str(organ="cor", values_default=dictionary_cor_default,
                      values_patho=dictionary_cor_patho)

    # Lunge
    dictionary_pulmo_default = {"Atemgeräusch": "vesikulär",
                                "Rasselgeräusche": "keine",
                                "Atemgeräusch_lokalisation": "",
                                "Klopfschall": "sonor",
                                "Klopfschall_lokalisation": "",
                                "Stimmfremitus": "regelrecht"
                                }

    dictionary_pulmo_patho = {"Atemgeräusch": ["", "vesikulär", "vesikulär abgeschwächt", "bronchial", "giemen", "brummen", "Stridor inspiratorisch", "Stridor expiratorisch", "Pleurareiben"],
                              "Rasselgeräusche": ["", "keine", "grobblasig", "feinblasig"],
                              "Atemgeräusch_lokalisation": lokalisation_lunge(),
                              "Klopfschall": ["", "hypersonor", "gedämpft", "tympanitisch"],
                              "Klopfschall_lokalisation": lokalisation_lunge(),
                              "Stimmfremitus": ["", "abgeschwächt", "verstärkt"]
                              }

    p = examinate_str(organ="pulmo", values_default=dictionary_pulmo_default,
                      values_patho=dictionary_pulmo_patho)

    # abdomen
    dictionary_abdomen_default = {"Haut": "unauffällig",
                                  "Darmgeräusche": "mittellebhaft",
                                  "Strömungsgeräusche": "keine",
                                  "Klopfschall": "tympanitisch",
                                  "Palpatorische_Schmerzen_NAS": "0",
                                  "Palpatorische_Schmerzen_lokalisation": "",
                                  "Leber": "nicht tastbar",
                                  "Milz": "nicht tastbar",
                                  "Klopfschmerzen": "keine"
                                  }
    dictionary_abdomen_patho = {"Haut": ["", "freitext?"],
                                "Darmgeräusche": ["", "vermindert", "aufgehoben", "gesteigert"],
                                "Strömungsgeräusche": ["", "über Aorta abdominalis", "A. renalis re", "A. renalis li", "A iliaca communis re", "A. iliaca communis li"],
                                "Klopfschall": ["", "gedämpft"],
                                "Palpatorische_Schmerzen_NAS": list_int(0, 10),
                                "Palpatorische_Schmerzen_lokalisation": lokalisation_abdomen(),
                                "Leber": ["", "vergrößert tastbar"],
                                "Milz": ["", "vergrößert tastbar"],
                                "Klopfschmerzen": ["", "über WS", "über Niere"]
                                }

    ab = examinate_str(organ="abdomen", values_default=dictionary_abdomen_default,
                       values_patho=dictionary_abdomen_patho)
    print("\n \n our documentation joined to one string: \n " +
          c + "\n" + p + "\n" + ab)

    # part 2 with fhir resource
    # these functions and documentations from https://community.intersystems.com/post/simple-example-fhir-client-python#1-fhir-client-python
    # not working yet...
    """
    # Now we want to create an fhir observation for our client

    # Get the id of the patient you want to attach the observation to
    id = Patient.parse_obj(patients_resources.search(
        family='familyname', given='givenname1').first().serialize()).id
    print("id of our patient : ", id)
        coding = Coding()
        coding.system = "https://loinc.org"
        coding.code = "1920-8"
        coding.display = "Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma"
        code = CodeableConcept()
        code.coding = [coding]
        code.text = "Aspartate aminotransferase [Enzymatic activity/volume] in Serum or Plasma"
              
    # Create a new observation using fhir.resources, we enter status and code inside the constructor since theuy are necessary to validate an observation
    observation0 = Observation(status="final", code=code)
    
    # Set our category in our observation, category which hold codings which are composed of system, code and display
    coding = Coding()
    coding.system = "https://terminology.hl7.org/CodeSystem/observation-category"
    coding.code = "laboratory"
    coding.display = "laboratory"
    category = CodeableConcept()
    category.coding = [coding]
    observation0.category = [category]
    
    # Set our effective date time in our observation
    observation0.effectiveDateTime = "2012-05-10T11:59:49+00:00"
    
    # Set our issued date time in our observation
    observation0.issued = "2012-05-10T11:59:49.565+00:00"
    
    # Set our valueQuantity in our observation, valueQuantity which is made of a code, a unir, a system and a value
    valueQuantity = Quantity()
    valueQuantity.code = "U/L"
    valueQuantity.unit = "U/L"
    valueQuantity.system = "https://unitsofmeasure.org"
    valueQuantity.value = 37.395
    observation0.valueQuantity = valueQuantity
    
    # Setting the reference to our patient using his id
    reference = Reference()
    reference.reference = f"Patient/{id}"
    observation0.subject = reference
    
    # Check our observation in the terminal
    print()
    print("Our observation : ", observation0)
    print()
    
    # Save (post) our observation0 using our client
    client.resource('Observation', **json.loads(observation0.json())).save()
        observation1 = Observation()
        print(observation1)
    
        # class Organ:
        #    organ_name: str
    
        # class Cor:
        #    Herztöne: str = "rein"
    """
