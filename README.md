# Vehicle Parking App

A multi-user 4-wheeler vehicle parking management web app built with **Flask**, **SQLite**, and **Bootstrap**. The app provides different roles for **Admin** (superuser) and **Users**, allowing for efficient parking lot and spot management, spot booking, and usage tracking.

## Tech Stack

- Backend: Flask
- Frontend: Jinja2, HTML5, CSS, Bootstrap
- Database: SQLite (created programmatically)

## Roles

### Admin (Superuser)

- No registration required
- Create, edit, and delete parking lots
- Auto-create parking spots based on lot capacity
- View all parking spots and their statuses
- Monitor all users and vehicle activity
- View summary charts

### User

- Register and log in
- View available parking lots
- Book the first available spot (auto-allotted)
- Release parking spot
- View personal parking history and summary charts

## Core Models

- **User:** `id`, `username`, `password`, `role`
- **Admin:** Pre-created on DB initialization
- **ParkingLot:** `id`, `location_name`, `price`, `address`, `pincode`, `max_spots`
- **ParkingSpot:** `id`, `lot_id (FK)`, `status`
- **Reservation:** `id`, `spot_id (FK)`, `user_id (FK)`, `start_time`, `end_time`, `cost_per_unit`

## Features

- Role-based dashboards (Admin and User)
- Parking spot allocation and release
- Timestamps for parking duration
- Admin CRUD operations for parking lots
- Charts and summaries for activity tracking
- Frontend and backend validation
- Optional API support (Flask/JSON)

## How to Run

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`
4. Open in browser: `http://127.0.0.1:5000`

## Notes

- Admin account is auto-created (no registration required)
- Database is created programmatically (no manual setup)
- Only supports 4-wheeler parking
