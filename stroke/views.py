import json
import requests
from django.shortcuts import render
from .ml_model.stroke_model import predict_stroke
from .utils import get_nearest_hospital, format_whatsapp_number, send_booking_message


def stroke_prediction_view(request):
    result = None
    hospital_info = None  # Stores hospital details if booking is done

    if request.method == 'POST':
        try:
            # Collect user input
            user_data = {
                'gender': request.POST['gender'],
                'age': request.POST['age'],
                'hypertension': request.POST['hypertension'],
                'heart_disease': request.POST['heart_disease'],
                'ever_married': request.POST['ever_married'],
                'work_type': request.POST['work_type'],
                'residence_type': request.POST['residence_type'],
                'avg_glucose_level': request.POST['avg_glucose_level'],
                'bmi': request.POST['bmi'],
                'smoking_status': request.POST['smoking_status'],
                'latitude': request.POST.get('latitude'),   # User's location (optional)
                'longitude': request.POST.get('longitude')
            }

            # Predict stroke
            prediction = predict_stroke(user_data)

            if prediction == 1:
                result = "⚠️ Stroke Detected! Booking hospital..."
                
                # Get nearest hospital
                hospital_data = get_nearest_hospital(user_data['latitude'], user_data['longitude'])
                print(hospital_data)
                hospital_name = hospital_data.get("hospital_name")
                hospital_phone = hospital_data.get("hospital_phone")

                if hospital_phone and hospital_phone != "Not Available":
                    formatted_number = format_whatsapp_number(hospital_phone)
                    
                    # Send automatic booking request
                    message_sid = send_booking_message(formatted_number, hospital_name)

                    hospital_info = {
                        "name": hospital_name,
                        "phone": formatted_number,
                        "message_sid": message_sid
                    }
                else:
                    result = "⚠️ Stroke Detected, but no hospital contact found!"
            else:
                result = "✅ No Stroke Detected."

        except KeyError as e:
            result = f"Invalid input: {str(e)}"
        except ValueError as e:
            result = f"Value error: {str(e)}"

    return render(request, 'index.html', {'result': result, 'hospital_info': hospital_info})
