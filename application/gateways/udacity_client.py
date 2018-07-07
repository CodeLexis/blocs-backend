import udacity


def create_client(email, password):
    return udacity.User(email, password)


def get_courses():
    c = udacity.Catalog()

    tracks = c.tracks()

    track_names = [t['name'] for t in tracks]
    web_dev_teachers = c.instructors('cs253')
    nd001_description = c.degree('nd001')['expected_learning']

    print(track_names, web_dev_teachers, nd001_description)

    return track_names, web_dev_teachers


if __name__ == '__main__':
    get_courses()
