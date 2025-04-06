# User Registration System

A complete web-based user registration system with secure authentication and user management.

## Features

- User registration with email verification
- Secure password handling
- User listing and management
- Modern, responsive UI
- Input validation (client and server-side)
- Error logging and debugging

## Prerequisites

- PHP 7.4 or higher
- MySQL 5.7 or higher
- Web server (Apache/Nginx)
- Composer (PHP package manager)
- Web browser

## Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd <project-directory>
   ```

2. **Database Setup**
   - Create a new MySQL database:
   ```sql
   CREATE DATABASE registration_db;
   ```
   - Import the database schema:
   ```bash
   mysql -u your_username -p registration_db < database.sql
   ```

3. **Configure Database Connection**
   - Copy `config.example.php` to `config.php`
   - Update database credentials in `config.php`:
   ```php
   define('DB_HOST', 'localhost');
   define('DB_USER', 'your_username');
   define('DB_PASS', 'your_password');
   define('DB_NAME', 'registration_db');
   ```

4. **Install Dependencies**
   ```bash
   composer install
   ```

5. **Set Up Web Server**
   - For Apache, ensure mod_rewrite is enabled
   - Point your web server to the project's public directory
   - Configure virtual host (optional)

6. **File Permissions**
   ```bash
   chmod 755 -R /path/to/project
   chmod 777 -R /path/to/project/logs
   ```

## Usage

1. **Access the Application**
   - Open your web browser
   - Navigate to: `http://localhost/your-project`

2. **Register a New User**
   - Click 'Register' on the homepage
   - Fill in the registration form
   - Submit the form

3. **View Registered Users**
   - Click 'View Users' link
   - Browse the list of registered users

## Security Features

- Password hashing using bcrypt
- CSRF protection
- XSS prevention
- SQL injection protection
- Input validation

## Troubleshooting

1. **Database Connection Issues**
   - Verify database credentials in `config.php`
   - Ensure MySQL service is running
   - Check database permissions

2. **Permission Errors**
   - Verify file permissions in logs directory
   - Check web server user permissions

3. **Form Submission Errors**
   - Enable debug mode in `config.php`
   - Check error logs

## Development

- Enable debug mode for development:
  ```php
  define('DEBUG_MODE', true);
  ```
- Check `logs/error.log` for debugging
- Use browser console for JavaScript debugging

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
