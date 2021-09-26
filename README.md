# Picture sharing

The project took about 20 hours to make.

## Set up the project

You can use the handy _setup\_and\_start.sh_ script.

### Create virtual environment

    python3 -m venv .hex

### Use the environment

    source ./.hex/bin/activate

### Install packages

    pip3 install -r requirements.txt

### Set up database

    python3 manage.py migrate

### Create uploads folder

    mkdir uploads

### Create superuser

    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('test_user', '', 'test_password')" |   python3 manage.py shell_plus

The superuser login and password are _test\_user_ and _test\_password_.

### Run the project

    python3 manage.py runserver


## API

| Function               | Endpoint                     | Request type | Comment                                               |
| ---------------------- | ---------------------------- | :----------: | ----------------------------------------------------- |
| Auth endpoint          | /api-auth/                   |     POST     |                                                       |
| Get images list        | /images/                     |     GET      |                                                       |
| Add image              | /images/                     |     POST     |                                                       |
| Get endpoint options   | /images/                     |   OPTIONS    |                                                       |
| Get image info         | /images/_ID_                 |     GET      |                                                       |
| Delete image           | /images/_ID_                 |    DELETE    |                                                       |
| Update image           | /images/_ID_                 |     PUT      |                                                       |
| Partially update image | /images/_ID_                 |    PATCH     |                                                       |
| Get endpoint options   | /images/_ID_                 |   OPTIONS    |                                                       |
| Get original image     | /uploads/_FILENAME_/         |     GET      | You can get this link from image list                 |
| Get scaled thumbnail   | /uploads/_FILENAME_/_HEIGHT_ |     GET      | You can create this link based on original image link |

_FILENAME_ is a string eg. /uploads/picture1.png/

__ is an integer specyfying thumbnail height eg. /uploads/picture1.png/200/
