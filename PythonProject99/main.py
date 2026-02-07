#pip install fastapi uvicorn jinja2
#py -m pip install fastapi uvicorn jinja2
# if will be pip not command

#py -m pip install fastapi uvicorn jinja2
from fastapi import FastAPI, Request, Form
from fastapi.openapi.utils import status_code_ranges
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
from starlette.routing import request_response

app = FastAPI()
templates = Jinja2Templates(directory="templates")

model = joblib.load('model.pkl')
le_marital = joblib.load('le_marital.pkl')
le_eduction = joblib.load('le_education.pkl')

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "education_options": list(le_eduction.classes_),
                                       "marital_options": list(le_marital.classes_)
                                       })

@app.get("/predict", response_class=HTMLResponse)
async def predict(request: Request,
                  age: int = Form(...),
                  income: int = Form(...),
                  rating: int = Form(...),
                  experience: int = Form(...),
                  Active_loan: int = Form(...),
                  payments: int = Form(...),
                  education: str = Form(...),
                  marital_status: str = Form(...)
                  ):

    try:

        education_encoded = le_eduction.transform([education]) [0]
        status_encoded = le_marital.transform([marital_status])[0]
        #
        #
        final_features = pd.DataFrame({
            "Возраст": [age],
            "доход": [income],
            "Кредитный рейтинг": [rating],
            "Длительность работы (лет)": [experience],
            "Активные кредиты": [active_loan],
            "просроченные платежи": [payments],
            "образование": [education_encoded],
            "Семейное положение": [status_encoded]

        })

        #
        prediction = model.predict(final_features)[0]
        probability = model.predict_proba(final_features)[0][1] * 100

       # form result
    result_text = f"result: {'Дефолт' if prediction == 1 else 'Нет дефолтаt'}\n" \
                  f"Вероятность дефолта: {probability:,2f}%"

    return templates.TemplateResponse('predict.html', {
        'request': request,
        'resultt': result_text,
        'prediction': prediction # Передаем 0 или 1 для стилизации
    })


    except Exception as e:
     #  Возращения пользователя на главную с сообщением об ошибке
     # в реальноом приложении можно сделать отдельнею страницу ошибок
     return templates.TemplateResponse("index.html", {
         "request": request,
         "education_options": list(le_eduction.classes_),
         "marital_options": list(le_marital.classes_),
         "error": f"Произошла ошибка: {e}"
     })




