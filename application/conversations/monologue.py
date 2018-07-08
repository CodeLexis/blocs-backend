import random

from flask import g


class Monologue(object):
    @classmethod
    def welcome(cls):
        welcome_statements = [
            "%s, welcome to Blocs! B)" % g.user.first_name,
            "Imagine taking classes with Facebook Live, instantly get help from"
            " developers across the world, seamlessly finding the right jobs & "
            "events.",
            "All from the comfort of Messenger. You're welcome! :O)"
        ]

        return welcome_statements

    @classmethod
    def ask_for_software_branch(cls):
        return random.choice([
            "What's the branch you're into?",
        ])

    @classmethod
    def apologize(cls):
        apologies = [
            "Come tomorrow, I'll probably understand that by then.",
            "I may not know what you mean now, but I'll find out!",
            "I haven't been programmed to understand that, yet.",
            "Hmmm... I'm sorry, but... I don't understand that"
        ]

        return random.choice(apologies)

    @classmethod
    def blush(cls):
        blushes = [
            "me.render(Reactions.blush())",
            "Awwwn... Thanks!",
            "It's what I was made to do. O:)",
            ':">'
        ]
        return random.choice(blushes)

    @classmethod
    def ask_for_course_title(cls):
        return "What are you planning to teach?"

    @classmethod
    def ask_for_event_title(cls):
        return "What event are you hosting?"

    @classmethod
    def compliment(cls):
        random_statements = [
            '%s, I must say... You have a great taste. ;)' % g.user.first_name,
            'Awesome! Get for two, please? :) :)',
            'Sweet!',
            'Terrific!',
            'Way to turn on the envy.',
            'Your friends are gonna be so damn jealous! B)',
            'Great choice, %s.' % g.user.first_name,
            'Fabulous!',
            'Excellent.',
            'This is such a fine product.',
            'Hmmn... Rad!'
        ]
        return random.choice(random_statements)

    @classmethod
    def compliment_software_branch(cls, branch):
        return "{}? That's so cool!".format(branch)

    @classmethod
    def greet(cls):
        random_statements = [
            "I'm glad you came back, %s!" % g.user.first_name,
            'Oh, hello %s!' % g.user.first_name,
            '%s! Welcome back. :)' % g.user.first_name,
        ]
        return random.choice(random_statements)

    @classmethod
    def random(cls):
        random_statements = [
            'You are the best.',
            'For you, I am here always.',
            'Forever at your service'
        ]
        return random.choice(random_statements)

    @classmethod
    def request_location(cls, scope=None):
        if scope:
            return "Would you rather like to see {} around you?".format(scope)

        return

    @classmethod
    def thank(cls):
        return

    @classmethod
    def thank_for_patronage(cls):
        return random.choice(
            ['Thanks for your patronage.', "We're grateful to know you :)"])

    @classmethod
    def take_to_all_courses(cls):
        return random.choice(
            ['Here are courses you could take...',
             "What's the skill you want to gain, %s?" % g.user.first_name,
             "Here are what we currently cover:",
             "Where would you like to start? ",
             "Have a look around...",
             "%s, what would you like to learn?" % g.user.first_name[0],]
        )

    @classmethod
    def take_to_course(cls):
        return

    @classmethod
    def take_to_all_events(cls):
        return random.choice([
            'Here are events you might like...',
            "Big events coming up:",
            "You might not want to miss these:"]
        )

    @classmethod
    def take_to_event(cls):
        return random.choice([
            "Here are the deets:",
            "Considering this, are we?",
            "Have a look"
        ])

    @classmethod
    def take_to_all_jobs(cls):
        return random.choice([
            'Looking to earn a few extra bucks? ;)',
            'I matched your skills with the offers'
        ])

    @classmethod
    def take_to_job(cls):
        return random.choice([
            "Here are the deets:",
            "Considering this, are we?",
            "Have a look"
        ])

    @classmethod
    def take_to_all_projects(cls):
        return random.choice([
            'Have a look',
            'People around the Bloc built these:',
            'Hopefully you get inspired by these:',
            '%s, you need to see these:' % g.user.first_name[0]
        ])

    @classmethod
    def take_to_project(cls):
        return random.choice([
            'The latest stories from %s:' % news_source.title.upper(),
            "Here are %s's headlines:" % news_source.title.upper(),
            'Headlines from %s:' % news_source.title.upper()
        ])

    @classmethod
    def process_completion(cls):
        return random.choice([
            "Done!", 'Task complete.', "It's done.", 'Done. Anything else?',
            'That was easy.', "Give me a minu... I'm done and back! B)",
            'All done! O:)'
        ])

    @classmethod
    def take_to_section(cls):
        all_statements = ['Here are the latest headlines:']
        return random.choice(all_statements)

    @classmethod
    def show_cart(cls):
        return random.choice(
            ['You added these to your cart recently:', 'Here it is:']
        )

    @classmethod
    def support_item_drop_decision(cls):
        return random.choice([
            "I'll take it back the shelf :)", "Just as well...",
            "You have an eye on your wallet it seems..."
        ])

    @classmethod
    def on_arrival_at_aisle(cls):
        return

    @classmethod
    def take_to_all_brief_sources(cls):
        return random.choice([
            "Here are your brief's sources:",
            "Your brief's sources, %s:" % g.user.first_name
        ])

    @classmethod
    def support_brief_source_drop_decision(cls):
        return random.choice([
            'Shedding some boring sections, I see :)',
            "It's best to have a slim pack, in my opinion."
        ])

    @classmethod
    def direct_to_all_brief_sources(cls):
        return random.choice([
            'You can access your Brief in the Menu below',
            'Tap "Brief" in the Menu below, to access them.',
        ])

    @classmethod
    def enquire_add_to_courses_offered(cls, news_source_title):
        news_source_title = news_source_title.upper()

        return random.choice([
            "Should I add %s's stories to your daily briefs?" %
            news_source_title,
            "Would you like stories from %s in your daily briefs?" %
            news_source_title,
        ])

    @classmethod
    def support_decision(cls):
        return random.choice([
            "Cool!", 'Fab!', 'You do have a good eye!'
        ])

if __name__ == '__main__':
    print(Monologue.direct_to_checkout())
