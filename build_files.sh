echo "BUILD START"
    pip install -r requirements.txt
    # mkdir -p staticfiles_build/static
    python3.9 manage.py collectstatic --noinput
    # python3.9 manage.py collectstatic
    echo "BUILD END"