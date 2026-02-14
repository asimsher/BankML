from fastapi import FastAPI
import joblib
import uvicorn
from pydantic import BaseModel

bank_app = FastAPI()
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')


class PersonSchema(BaseModel):
    person_age: int
    person_gender: str
    person_education: str
    person_incom:float
    person_emp_exp:int
    person_home_ownership:str
    loan_amnt:float
    loan_intent:str
    loan_int_rate:float
    loan_percent_income:float
    credit_score:int
    previous_loan_defaults_on_file:str



@bank_app.post('/predict/')
async def predict(person: PersonSchema):
    person_dict = person.dict()

    new_person_gender = person_dict.pop('person_gender')
    person_gender1_0 = [1 if new_person_gender == 'female' else 0]


    new_person_education = person_dict.pop('person_education')
    person_education1_0 = [1 if new_person_education == 'Bachelor' else 0,
                           1 if new_person_education == 'Doctorate' else 0,
                           1 if new_person_education == 'High School' else 0,
                           1 if new_person_education == 'Master' else 0,
                           ]
    new_home_ownership = person_dict.pop('person_home_ownership')
    home_ownership1_0 = [1 if new_home_ownership == 'OTHER' else 0,
                         1 if new_home_ownership == 'OWN' else 0,
                         1 if new_home_ownership == 'RENT' else 0,
                         ]

    new_loan_intent = person_dict.pop('loan_intent')
    loan_intent1_0 = [1 if new_loan_intent == 'EDUCATION' else 0,
                      1 if new_loan_intent == 'HOMEIMPROVEMENT' else 0,
                      1 if new_loan_intent == 'MEDICAL' else 0,
                      1 if new_loan_intent == 'PERSONAL'else 0,
                      1 if new_loan_intent == 'VENTURE' else 0,
                      ]




    new_defaults = person_dict.pop('previous_loan_defaults_on_file')
    new_defaults1_0 = [1 if new_defaults == 'Yes' else 0]

    features = (list(person_dict.values()) + person_gender1_0 + person_education1_0 + home_ownership1_0
                + loan_intent1_0 + new_defaults1_0)


    scaled_data = scaler.transform([features])
    pred = model.predict(scaled_data)[0]
    prob = model.predict_proba(scaled_data)[0][1]

    return {'approved': bool(pred), 'probability': round(prob, 2)}




if __name__ == '__main__':
    uvicorn.run(bank_app, host='127.0.0.1', port=8002)