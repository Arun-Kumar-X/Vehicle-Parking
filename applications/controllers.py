from flask import render_template, request, redirect, url_for
from flask import current_app as app
from .models import *
from datetime import datetime

# Login Route
@app.route('/')
def root_redirect():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if username == 'Admin' and password == '54321':   
            return redirect('/admin')

        if user:
            if user.password == password:
                return redirect(url_for('user_dashboard', user_id=user.id))
            else:
                return "Incorrect password. Please try again."
        else:
            return "User not found. Please check your username."
            
    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        full_name = request.form['full_name']
        address = request.form['address']
        pin_code = request.form['pin_code']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match. Please try again."
        
        if User.query.filter_by(username=username).first():
            return "Username already exists. Please choose a different username."
        
        new_user = User(username=username, full_name=full_name, address=address, pin_code=pin_code, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/login')
    
    return render_template('signup.html')

# Admin Dashboard Route
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    lots = ParkingLot.query.all()
    spots = ParkingSpot.query.all()
    counts = {lot.id: ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count() for lot in lots}

    return render_template('admin-dash.html', lots=lots, spots=spots, counts=counts)

# Add Parking Lot Route
@app.route('/new_lot', methods=['GET', 'POST'])
def new_parking_lot():
    if request.method == 'POST':
        lot_name = request.form['lot']
        address = request.form['address']
        pin_code = request.form['pin-code']
        price = request.form['price']
        max_spots = int(request.form['spots'])

        new_lot = ParkingLot(lot_name=lot_name, price=price, max_spots=max_spots, address=address,  pincode=pin_code,)
        db.session.add(new_lot)
        db.session.commit()

        for _ in range(max_spots):
            new_spot = ParkingSpot(lot_id=new_lot.id, status='A')
            db.session.add(new_spot)
        db.session.commit()

        return redirect('/admin')

    next_id = ParkingLot.query.order_by(ParkingLot.id.desc()).first()
    id = next_id.id + 1 if next_id else 1
    return render_template('new-lot.html', id=id)

# View Parking Spot Route
@app.route('/view/<int:lot_id>/<int:spot_id>', methods=['GET', 'POST'])
def view_parking_lot(lot_id, spot_id):
    spot = ParkingSpot.query.get(spot_id)

    if request.method == 'POST':
        if spot.status == 'A':
            spot.status = 'O'
        else:
            spot.status = 'A'
        db.session.commit()
        return redirect(f'/view/{lot_id}/{spot_id}')
    
    return render_template('view-spot.html', lot_id=lot_id, spot_id=spot_id, status=spot.status)

# Occupied Parking Slot Route
@app.route('/occupied/<int:spot_id>', methods=['GET', 'POST'])
def occupied_parking_slot(spot_id):
    res = Reservation.query.filter_by(spot_id=spot_id).order_by(Reservation.id.desc()).first()
    if not res:
        message = "⚠️ No reservation found for this parking spot."
        return render_template('occupied-spot.html', message=message, spot_id=spot_id)

    spot = ParkingSpot.query.get(res.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)
    user = User.query.get(res.user_id)

    if request.method == 'POST':
        return redirect(url_for('release_parking_spot', user_id=res.user_id, spot_id=spot_id))

    return render_template('occupied-spot.html', res=res, lot=lot, user=user, spot_id=spot_id)

# Edit Parking Lot Route
@app.route('/edit/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        lot.lot_name = request.form['lot']
        lot.address = request.form['address']
        lot.pincode = int(request.form['pin-code'])
        lot.price = float(request.form['price'])

        new_max_spots = int(request.form['spots'])
        current_count = len(lot.spots)

        if new_max_spots > current_count:
            for _ in range(new_max_spots - current_count):
                new_spot = ParkingSpot(lot_id=lot.id, status='A')
                db.session.add(new_spot)

        elif new_max_spots < current_count:
            spots_to_delete = ParkingSpot.query.filter(ParkingSpot.lot_id == lot.id).order_by(ParkingSpot.id.desc()).limit(current_count - new_max_spots).all()
            for spot in spots_to_delete:
                db.session.delete(spot)

        lot.max_spots = new_max_spots
        db.session.commit()

        return redirect('/admin')

    return render_template('edit-lot.html', lot=lot)

# Delete Parking Lot Route
@app.route('/delete/<int:lot_id>', methods=['GET'])
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get(lot_id)
    if lot:
        db.session.delete(lot)
        db.session.commit()
    return redirect('/admin')

# Registered Users Route
@app.route('/registered_user', methods=['GET'])
def registered_users():
    users = User.query.all()
    return render_template('users.html', users=users)

# Summary Route
@app.route('/summary', methods=['GET'])
def summary():
    reservations = Reservation.query.all()
    return render_template('summary.html', reservations=reservations)

# User Dashboard Route
@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_dashboard(user_id):
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    user = User.query.filter_by(id=user_id).first()

    pincode = None

    if request.method == 'POST':
        form_pincode = request.form.get('pincode')
        if form_pincode:
            pincode = form_pincode 
    lots = ParkingLot.query.filter_by(pincode=pincode).all()

    availability = {
        lot.id: ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        for lot in lots
    }
    return render_template('user-dash.html', lots=lots, user=user, reservations=reservations, availability=availability, pincode=pincode)

# Reserve Parking Spot Route
@app.route('/reserve/<int:user_id>/<int:lot_id>', methods=['GET', 'POST'])
def reserve_parking_spot(user_id, lot_id):
    lot = ParkingLot.query.get(lot_id)
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    
    if not spot:
        return "⚠️ No available spot in this lot right now."

    if request.method == 'POST':
        vehicle_num = request.form['vehicle_num']
        start_time_str = request.form['start_time']

        now = datetime.now()
        start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")

        reservation = Reservation(user_id=user_id, spot_id=spot.id, vehicle_num=vehicle_num, start_time=start_time, end_time=None, price=lot.price)
        spot.status = 'O'
        
        db.session.add(reservation)
        db.session.commit()
        
        return redirect(url_for('user_dashboard', user_id=user_id))

    return render_template('reserve-spot.html', lot=lot, spot=spot, user_id=user_id)

# Release Parking Spot Route
@app.route('/release/<int:user_id>/<int:spot_id>', methods=['GET', 'POST'])
def release_parking_spot(user_id, spot_id):
    res = Reservation.query.filter_by(spot_id=spot_id).order_by(Reservation.id.desc()).first()
    spot = ParkingSpot.query.get(spot_id)
    lot = ParkingLot.query.get(spot.lot_id)

    if not res:
        return "⚠️ No active reservation found."

    now = datetime.now()
    duration = (now - res.start_time).total_seconds() / 3600
    price = max(duration * lot.price, lot.price)

    if request.method == 'POST':
        res.end_time = now
        res.price = round(price, 2)
        spot.status = 'A'

        db.session.commit()
        return redirect(url_for('user_dashboard', user_id=user_id))

    return render_template('release-spot.html', res=res, lot=lot, user_id=user_id, current_time=now.strftime("%H:%M    (%d-%m-%Y)"), price=round(price, 2), spot_id=spot_id)