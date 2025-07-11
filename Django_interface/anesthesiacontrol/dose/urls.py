from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Home page
    path("home/", views.home, name="home"),  # Home page with form
    path("start_monitoring/", views.start_monitoring, name="start_monitoring"),  # Start monitoring
    path("fetch_data/", views.fetch_data, name="fetch_data"),  # Fetch sensor data
    path("stop_monitoring/", views.stop_monitoring, name="stop_monitoring"),  # Stop monitoring
      # Monitoring page (add this line)
    path("login/", views.login_view, name="login"),  # Login page
    path("patient_database/", views.patient_database, name="patient_database"), 
    path("login_success/", views.login_success,name="login_success"),
    path('start_surgery/', views.start_surgery, name='start_surgery'),
    path('stop_surgery/', views.stop_surgery, name='stop_surgery'), 
    path('predict_data/', views.predict_data, name='predict_data'),
    path('start_surgery/', views.start_surgery, name='start_surgery'),
    path('stop_surgery/', views.stop_surgery, name='stop_surgery'),
    path('get_latest_predictions/', views.get_latest_predictions, name='get_latest_predictions'),
    # Patient database
    
]