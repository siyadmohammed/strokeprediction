import json
import requests
from django.shortcuts import render
from .ml_model.stroke_model import predict_stroke
from .utils import get_nearest_hospitals
from .app import get_stroke_precautions
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('stroke_prediction')  
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def stroke_prediction_view(request):
    result = None
    hospital_info = None
    precautions_info = None  # New variable for precautions

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
                'latitude': request.POST.get('latitude'),
                'longitude': request.POST.get('longitude')
            }
            print(user_data)
            # Predict stroke
            prediction = predict_stroke(user_data)

            if prediction == 1:
                result = "⚠️ Stroke Detected!"
                
                # Get nearest hospitals
                hospital_data = get_nearest_hospitals(user_data['latitude'], user_data['longitude']) 
                # Ensure hospital data is valid
                if "places" in hospital_data and isinstance(hospital_data["places"], list) and len(hospital_data["places"]) > 0:
                    nearest_hospital = hospital_data["places"][0] 

                    # Extract hospital details safely
                    hospital_name = nearest_hospital.get("displayName", "Unknown Hospital")
                    hospital_phone = nearest_hospital.get("internationalPhoneNumber", "Not Available")
                    hospital_website = nearest_hospital.get("websiteUri", "Not Available")

                    hospital_info = {
                        "name": hospital_name,
                        "phone": hospital_phone,
                        "website": hospital_website
                    }

                    hospital_detail = f"\n🏥 Nearest Hospital: {hospital_name}\n📞 Contact: {hospital_phone}\n Website: {hospital_website}"
                    formatted_result = hospital_detail.replace("\n", "<br>")
                else:
                    hospital_detail = "\n🚑 No nearby hospitals found."
                    formatted_result = hospital_detail.replace("\n", "<br>")

                # Get stroke precautions
                precautions_info = get_stroke_precautions()
                
                # Append hospital details and precautions to the result
                result += formatted_result
            else:
                result = "✅ No Stroke Detected."

        except KeyError as e:
            result = f"Invalid input: {str(e)}"
        except ValueError as e:
            result = f"Value error: {str(e)}"
        except Exception as e:
            result = f"Unexpected error: {str(e)}"

    return render(request, 'finalindex.html', {
        'result': result, 
        'hospital_info': hospital_info,
        'precautions_info': precautions_info
    })

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')