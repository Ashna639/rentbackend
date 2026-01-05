# ⚙️ RentSpace API - Backend

This is the robust backend engine for the **Rental Space Management System**. It provides a secure RESTful API to handle user accounts, property data, and business logic.

## 🔗 Live API
- **API Root:** [https://rentbackend-mfqg.onrender.com/api/](https://rentbackend-mfqg.onrender.com/api/)
- **Admin Dashboard:** [https://rentbackend-mfqg.onrender.com/admin/](https://rentbackend-mfqg.onrender.com/admin/)

## 🛠️ Tech Stack
- **Framework:** Django & Django REST Framework (DRF)
- **Database:** Neon Serverless PostgreSQL
- **Hosting:** Render (Free Tier)
- **Auth:** Simple JWT (JSON Web Tokens)
- **Deployment:** Gunicorn & WhiteNoise

## ✨ Key Features
- **User Roles:** Custom logic to differentiate between Sellers and Consumers.
- **Security:** JWT-based authentication for protected routes (Creating/Editing listings).
- **Database:** Fully managed PostgreSQL on Neon for high availability.
- **CORS Configured:** Securely allows requests from the Vercel frontend.

## ⚙️ Local Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_BACKEND_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_BACKEND_REPO_NAME.git)
   cd YOUR_BACKEND_REPO_NAME



   ### One Final Pro-Tip:
Since you are using **Neon**, it’s a good idea to mention "Serverless Postgres" in your conversations with recruiters. It shows you are up-to-date with modern database scaling!

**Would you like me to show you how to add a "Deploy to Render" button to your backend README so others can clone and host it easily?**
