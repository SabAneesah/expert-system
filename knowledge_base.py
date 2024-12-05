from experta import *

class DiabetesExpertSystemKB(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.reset()

    def add_fact(self, fact_name, value):
        # Ensure all values are strings before declaring
        if isinstance(value, (int, float)):
            value = str(value)
        self.declare(Fact(fact_name=fact_name, value=value))

    @Rule(Fact(fact_name="symptoms", value=MATCH.symptom))
    def check_symptoms(self, symptom):
        if isinstance(symptom, str) and "Frequent urination" in symptom:
            self.declare(Fact(diabetes_risk="Possible Diabetes - Symptoms indicate need for checkup"))

    @Rule(Fact(fact_name="fasting_blood_sugar", value=MATCH.fbs))
    def check_fbs(self, fbs):
        try:
            fbs_value = float(fbs)
            if fbs_value > 126:
                self.declare(Fact(diabetes_risk="High Fasting Blood Sugar - Consult a doctor"))
            elif fbs_value < 70:
                self.declare(Fact(diabetes_risk="Low Fasting Blood Sugar - Take precaution"))
        except ValueError:
            pass  # Invalid value; ignore this fact

    @Rule(Fact(fact_name="hba1c", value=MATCH.hba1c))
    def check_hba1c(self, hba1c):
        try:
            hba1c_value = float(hba1c)
            if hba1c_value >= 6.5:
                self.declare(Fact(diabetes_risk="High HbA1c - Indicates Diabetes"))
            elif hba1c_value >= 5.7:
                self.declare(Fact(diabetes_risk="Borderline HbA1c - Risk of Diabetes"))
        except ValueError:
            pass  # Invalid value; ignore this fact

    def run_inference_engine(self):
        self.reset()
        self.run()
        results = {}
        for fact in self.facts.values():
            if isinstance(fact, Fact) and 'diabetes_risk' in fact:
                results[fact['diabetes_risk']] = True
        return results
