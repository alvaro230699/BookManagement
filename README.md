# BookManagement

Programming challenge to create a book management system which implement CRUD operations for book model and a aggregation API to calculate
the yearly average price of published books.

## Installation

### Prerequisites

- Python ^3.8
- Pip ^21.1

### Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create and activate the virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the requirements file**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create the env file and setup it accordingly with the .env.example**

   ```bash
   touch .env
   ```

5. **Run Django migrations and seed database:**
   Perform migrations and database seeding:

   ```bash
   python manage.py migrate
   python manage.py dbseed
   ```

6. **Verify the server:**
   Open your web browser and visit [https://localhost:8000](https://localhost:8000).

## Documentation

Open your web browser and visit [https://localhost:8000/api/documentation](https://localhost:8000/api/documentation).

## References

1. [Django](https://www.djangoproject.com/)
