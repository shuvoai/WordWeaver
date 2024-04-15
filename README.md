<h1>Word Weaver</h1>

<h2>Overview</h2>
<p>Word Weaver is a Django project designed to manage simple blogging</p>
<ul>
    <li>Token authentication for secure user login</li>
    <li>Admin panel for managing User, blogs, and comments</li>
    <li>Permission handling for user authorization</li>
    <li>Create, edit, delete, and view blogs and comments</li>
</ul>

<h2>Getting Started</h2>
<h3>Prerequisites</h3>
<ul>
    <li>Python 3.x</li>
    <li>Django 3.x</li>
    <li>Django REST framework</li>
    <li>Django Rest Framework Token auth</li>
    <li>MySql</li>
</ul>
<h3>Installation</h3>
<ol>
    <li>Clone the repository</li>
<pre>git clone https://github.com/your-username/WordWeaver.git</pre>
    <li>Create a virtual environment and activate it</li>
    <pre>python -m venv env</pre>
    <pre>source env/bin/activate</pre>
    <li>Install dependencies</li>
    <pre>pip install -r requirements.txt</pre>
    <li>Create a .env file in the root directory with the following information:</li>
    <pre>
    SECRET_KEY=<your Django secret key>
    DEBUG=True
    DB_NAME=<your MySQL database name>
    DB_USER=<your MySQL database user>
    DB_PASSWORD=<your MySQL database password>
    DB_HOST=<your MySQL host>
    DB_PORT=<your MySQL port>
    </pre>
    <li>Run migrations</li>
    <pre>python manage.py makemigrations</pre>
    <pre>python manage.py migrate</pre>
    <li>Create a superuser</li>
    <pre>python manage.py createsuperuser</pre>
    <li>Start the server</li>
    <pre>python manage.py runserver</pre>
</ol>
    <p>The system will be running on http://localhost:8000</p>
<h3>Checking test cases</h3>
<ol>
    <li>check all the test case</li>
    <pre>python manage.py test</pre>
    <li>check the test cases of a specific app</li>
    <pre>python manage.py test your_app_name</pre>
</ol>
<h3>Docker</h3>
<ol>
    <li>Build the Docker image</li>
    <pre>docker build -t wordweaver .</pre>
    <li>Run the Docker container</li>
    <pre>docker-compose up</pre>
</ol>

