from datetime import datetime
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from utility import generate_otp, send_otp_email, send_otp
from homepage.models import Registration


def homepage(request):
    context = {
        'hero': {
            'title': 'AI-Powered Financial <span>Fraud Detection</span>',
            'subtitle': 'Protect your transactions with advanced machine learning algorithms that detect and prevent fraud in real-time.',
            'button_text': 'Get Started'
        },
        'stats': [
            {'icon': 'fas fa-shield-check', 'value': 99.8, 'suffix': '%', 'label': 'Detection Accuracy'},
            {'icon': 'fas fa-arrow-right-arrow-left', 'value': 50000, 'suffix': '+', 'label': 'Transactions Protected'},
            {'icon': 'fas fa-clock', 'value': 24, 'suffix': '/7', 'label': 'Real-time Monitoring'},
            {'icon': 'fas fa-user-shield', 'value': 1000, 'suffix': '+', 'label': 'Active Users'}
        ],
        'features': [
            {
                'icon': 'fas fa-robot',
                'title': 'AI & Machine Learning',
                'description': 'State-of-the-art algorithms including XGBoost, Random Forest, and Neural Networks for accurate fraud detection.',
                'link': '#'
            },
            {
                'icon': 'fas fa-chart-line',
                'title': 'Real-time Analytics',
                'description': 'Monitor transactions as they happen with live dashboards and instant alert systems.',
                'link': '#'
            },
            {
                'icon': 'fas fa-network-wired',
                'title': 'Graph Analysis',
                'description': 'Detect complex fraud networks and patterns using advanced graph-based algorithms.',
                'link': '#'
            },
            {
                'icon': 'fas fa-bell',
                'title': 'Smart Alert System',
                'description': 'Automated alerts via email and SMS for immediate action on suspicious transactions.',
                'link': '#'
            },
            {
                'icon': 'fas fa-database',
                'title': 'Data Integration',
                'description': 'Seamlessly integrate with multiple data sources including credit cards, bank accounts, and customer profiles.',
                'link': '#'
            },
            {
                'icon': 'fas fa-shield-alt',
                'title': 'Risk Scoring Engine',
                'description': 'Comprehensive risk assessment with customer, destination, and transaction risk scoring.',
                'link': '#'
            }
        ],
        'steps': [
            {
                'icon': 'fas fa-cloud-upload-alt',
                'title': 'Data Ingestion',
                'description': 'Upload transaction data or connect to real-time data streams for continuous monitoring.'
            },
            {
                'icon': 'fas fa-brain',
                'title': 'AI Analysis',
                'description': 'Our ML models analyze patterns, detect anomalies, and identify potential fraud in milliseconds.'
            },
            {
                'icon': 'fas fa-bell',
                'title': 'Action & Alert',
                'description': 'Get instant alerts for suspicious transactions and take immediate action to prevent fraud.'
            }
        ],
        'testimonials': [
            {
                'quote': 'FraudDetect has reduced our fraud losses by 85% in just 3 months. The real-time detection is remarkable.',
                'author': 'Sarah Johnson',
                'role': 'CFO, TechBank Inc.'
            },
            {
                'quote': 'The AI models are incredibly accurate. We can now detect fraud patterns that we missed before.',
                'author': 'Michael Chen',
                'role': 'Security Director, FinSecure'
            },
            {
                'quote': 'Easy to integrate and the dashboard provides all the insights we need to make informed decisions.',
                'author': 'Emily Rodriguez',
                'role': 'Risk Manager, GlobalPay'
            }
        ]
    }
    return render(request, 'homepage/homepage.html', context)

def choose(request):

    return render(request,'homepage/choose.html')

def register(request):
    # form = StudentRegistrationForm()
    return render(request,'homepage/registration.html')




def submit_registration(request):

    if request.method == "POST":

        # =========================
        # GET DATA FROM HTML
        # =========================
        full_name = request.POST.get("full_name")
        date_of_birth = request.POST.get("date_of_birth")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        terms = request.POST.get("terms")

        # =========================
        # CHECK PASSWORD
        # =========================
        if password != confirm_password:

            return render(
                request,
                "homepage/registration.html",
                {
                    "message": "Passwords do not match."
                }
            )

        # =========================
        # CHECK TERMS
        # =========================
        if not terms:

            return render(
                request,
                "homepage/registration.html",
                {
                    "message": "Please accept Terms & Conditions."
                }
            )

        # =========================
        # STORE DATA IN SESSION
        # =========================
        request.session["form_data"] = {
            "full_name": full_name,
            "date_of_birth": date_of_birth,
            "email": email,
            "phone": phone,
            "address": address,
            "password": password,
        }

        # =========================
        # GENERATE OTP
        # =========================
        otp = generate_otp()

        # =========================
        # SEND OTP
        # =========================
        send_otp_email(
            email,
            otp,
            "Registration"
        )

        # =========================
        # STORE OTP
        # =========================
        request.session["email"] = email
        request.session["otp"] = otp

        # =========================
        # SHOW OTP
        # =========================
        return render(
            request,
            "homepage/registration.html",
            {
                 'message': 'OTP sent to your email',
                'otp': otp,
                'show_otp': True,  # 🔥 THIS IS REQUIRED
            }
        )
    else:
        print("FORM ERRORS:")

    # =========================
    # FIRST TIME OPENING PAGE
    # =========================
    return render(
        request,
        "homepage/registration.html"
    )


def verify_otp(request):

    # ==========================================
    # GET REQUEST
    # ==========================================
    if request.method != "POST":
        return render(
            request,
            "homepage/verify_otp.html"
        )

    # ==========================================
    # GET OTP
    # ==========================================
    user_otp = request.POST.get("otp")
    session_otp = request.session.get("otp")

    print("USER OTP:", user_otp)
    print("SESSION OTP:", session_otp)

    # ==========================================
    # CHECK OTP
    # ==========================================
    if not user_otp or not session_otp:

        return render(
            request,
            "homepage/verify_otp.html",
            {
                "error": "OTP expired. Please register again."
            }
        )

    if str(user_otp).strip() != str(session_otp).strip():

        return render(
            request,
            "homepage/verify_otp.html",
            {
                "error": "Invalid OTP."
            }
        )

    # ==========================================
    # GET REGISTRATION DATA
    # ==========================================
    data = request.session.get("form_data")

    if not data:

        return render(
            request,
            "homepage/verify_otp.html",
            {
                "error": "Session expired. Please register again."
            }
        )

    # ==========================================
    # GET FORM DATA
    # ==========================================
    full_name = data.get("full_name")
    date_of_birth = data.get("date_of_birth")
    email = data.get("email")
    phone = data.get("phone")
    address = data.get("address")
    password = data.get("password")

    # ==========================================
    # CHECK REQUIRED DATA
    # ==========================================
    if not full_name or not date_of_birth or not email or not password:

        return render(
            request,
            "homepage/verify_otp.html",
            {
                "error": "Registration data is incomplete."
            }
        )

    # ==========================================
    # CONVERT DATE
    # ==========================================
    try:

        if isinstance(date_of_birth, str):

            date_of_birth = datetime.strptime(
                date_of_birth,
                "%Y-%m-%d"
            ).date()

    except ValueError:

        return render(
            request,
            "homepage/verify_otp.html",
            {
                "error": "Invalid date of birth."
            }
        )

    # ==========================================
    # CHECK EXISTING EMAIL
    # ==========================================
    if Registration.objects.filter(email=email).exists():

        return render(
            request,
            "homepage/homepage.html",
            {
                "error": "An account with this email already exists."
            }
        )

    # ==========================================
    # CREATE REGISTRATION
    # ==========================================
    registration = Registration(
        full_name=full_name,
        date_of_birth=date_of_birth,
        email=email,
        phone=phone,
        address=address
    )

    # ==========================================
    # HASH PASSWORD
    # ==========================================
    registration.set_password(password)

    # ==========================================
    # SAVE USER
    # ==========================================
    registration.save()

    # ==========================================
    # CLEAR SESSION
    # ==========================================
    request.session.flush()

    # ==========================================
    # GO TO HOMEPAGE
    # ==========================================
    return render(
        request,
        "homepage/homepage.html",
        {

            "success_registration": True,
            "registration": registration
        }
    )

def login(request):
    show_otp = request.session.get('otp_show', False)

    request.session['otp_show'] = False



    return render(request, 'homepage/login.html', {
        'show_otp': show_otp
    })

@ensure_csrf_cookie
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":

        login_type = request.POST.get("login_type")

        # =====================================================
        # EMAIL LOGIN
        # =====================================================

        if login_type == "email":

            email = request.POST.get("email", "").strip()
            password = request.POST.get("password", "")

            print(password)
            user_obj = User.objects.filter(email=email).first()

            if user_obj:
                print("USERNAME:", user_obj.username)
                print("PASSWORD VALID:", user_obj.check_password(password))

                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            else:
                user = None

            if user is not None:

                auth_login(request, user)

                # Get registration/customer
                registration = Registration.objects.filter(
                    email=email
                ).first()

                if registration:
                    request.session["email"] = registration.email
                    request.session["full_name"] = registration.full_name

                    print("FULL NAME:", registration.full_name)

                return redirect("dashboard:dashboard")

            else:

                messages.error(
                    request,
                    "Invalid email or password"
                )

            # ---------------- OTP LOGIN ----------------

        elif login_type == "otp":

            identifier = request.POST.get("otp_login")  # ✅ FIXED


            otp = generate_otp()



            request.session['identifier'] = identifier
            print(identifier)
            if "@" in identifier:

                send_otp_email(email=identifier, otp=otp, catagory="login")
                print(identifier)
                message = "OTP sent to your email"
                request.session['otp'] = otp
                request.session['message'] = message
                request.session['otp_show'] = True

                request.session['otp_show'] = True

                return render(request, "homepage/login.html", {
                    "otp_show": True,

                })



            else:

                message = "OTP sent to your mobile"
                request.session['otp'] = otp
                request.session['message'] = message
                request.session['otp_show'] = True
                identifier = "+91" + identifier
                request.session['otp_show'] = True

                request.session['identifier'] =  identifier

                send_otp(

                    phone_number=identifier,



                    otp=otp

                )

                return render(request, 'homepage/login.html', {

                    "otp_show": True

                })


    return render(request, "homepage/login.html")

def verify_otp2(request):

    if request.method == "POST":

        user_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        identifier = request.session.get("identifier")
        if '@' not in identifier:
            identifier = identifier[3:]


        # Check OTP
        if str(user_otp) == str(session_otp):

            print("Entered OTP correct")

            if identifier:

                identifier = identifier.strip()

            # First check email
            customer = Registration.objects.filter(
                email=identifier
            ).first()

            # If not found, check phone
            if not customer:
                customer = Registration.objects.filter(
                    phone=identifier
                ).first()



            if customer:

                request.session["email"] = customer.email
                request.session["full_name"] = customer.full_name



                return redirect("dashboard:dashboard")

            else:

                print("No customer found for:", repr(identifier))

                messages.error(
                    request,
                    "Customer not found."
                )

        else:

            messages.error(
                request,
                "Invalid OTP."
            )

    return render(request, "homepage/login.html")