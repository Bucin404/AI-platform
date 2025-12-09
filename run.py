"""Application entry point."""
from app import create_app, db
from app.models.user import User
import os

app = create_app(os.environ.get('FLASK_ENV', 'default'))


@app.shell_context_processor
def make_shell_context():
    """Make database models available in shell."""
    return {'db': db, 'User': User}


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized.')


@app.cli.command()
def create_admin():
    """Create admin user."""
    from config import Config
    
    admin = User.query.filter_by(email=Config.ADMIN_EMAIL).first()
    if admin:
        print(f'Admin user already exists: {admin.email}')
        return
    
    admin = User(
        username='admin',
        email=Config.ADMIN_EMAIL,
        role='admin',
        tier='premium'
    )
    admin.set_password(Config.ADMIN_PASSWORD)
    db.session.add(admin)
    db.session.commit()
    
    print(f'Admin user created: {admin.email}')
    print(f'Password: {Config.ADMIN_PASSWORD}')
    print('Please change the password after first login!')


if __name__ == '__main__':
    # WARNING: Debug mode should NEVER be enabled in production
    # It allows arbitrary code execution through the debugger
    # Set DEBUG=False in production environment variables
    import os
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    if debug_mode:
        print("WARNING: Running in DEBUG mode. This should ONLY be used in development!")
        print("Set DEBUG=False in production to prevent security vulnerabilities.")
    
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
