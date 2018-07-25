import random

from flask import g


class Monologue(object):
    @classmethod
    def welcome(cls):
        welcome_statements = [
            "There's a lot that Facebook's Developer Circles hasn't clearly "
            "tackled! I mean...",

            "Welcome to Blocs, %s! B)" % g.user.first_name[0],
            "Those features will be added to your Facebook page, at no extra "
            "install or signup. But first off..."
        ]

        return welcome_statements

    @classmethod
    def echo_user_details(cls):
        return str(g.user.as_json())

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
    def compliment_location(cls):
        return "Always wanted to visit {}!".format(
            g.user.locations[-1].town)

    @classmethod
    def compliment_software_branch(cls, branch):
        return "{}? That's so cool!".format(branch)

    @classmethod
    def empty_resource(cls, scope):
        return random.choice([
            'There is no {} in any of your Blocs yet.'.format(scope),
            'There is currently no {} in any of your Blocs.'.format(scope),
            'Awwn! No {} in any your Blocs.'.format(scope)
        ])

    @classmethod
    def request_facebook_login(cls, scope=None, required=False):
        if required:
            statement = random.choice([
                "You need to connect your Facebook account, first.",
                "You haven't connected your Facebook account yet.",
                "Oops.. You would first have to connect your Facebook "
                "account, {}".format(g.user.first_name[0])
            ])

        else:
            statement = random.choice([
                "Blocs depends on Facebook for the best parts of {}".format(
                    scope),
                "You need to connect your Facebook account for Blocs' {}".format(
                    scope)
            ])

        return statement

    @classmethod
    def greet(cls):
        random_statements = [
            "I'm glad you came back, %s!" % g.user.first_name,
            'Oh, hello %s!' % g.user.first_name,
            '%s! Welcome back. :)' % g.user.first_name,
        ]
        return random.choice(random_statements)

    @classmethod
    def instruct_on_posting_feeds(cls):
        return (
            "You can share anything to the devs in your Blocs, Facebook and "
            "Instagram, just by including the hash-tag #Blocs in any message you send "
            "me! B)"
        )

    @classmethod
    def random(cls):
        random_statements = [
            'You are the best.',
            'For you, I am here always.',
            'Forever at your service'
        ]
        return random.choice(random_statements)

    @classmethod
    def request_location_for_bloc(cls):
        return "Join the Bloc closest to you"

    @classmethod
    def request_location(cls, scope=None):
        responses_with_scope = [
            "Would you like to see {} around you?",
            "Find the {} around you would be better",
            "Several {} could be around you"
        ]

        response = [
            "First off, I have to know where you are",
            "I need to know where you are, first, though",
            "But first... I have to know your location",
        ]

        if scope:
            return random.choice(responses_with_scope).format(scope)

        return random.choice(response)

    @classmethod
    def thank(cls):
        return

    @classmethod
    def thank_for_patronage(cls):
        return random.choice(
            ['Thanks for your patronage.', "We're grateful to know you :)"])

    @classmethod
    def take_to_all_blocs(cls):
        return "Now %s, dive-in and join other developers (Y)" % \
               g.user.first_name

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
    def take_to_events_interested_in(cls):
        return random.choice([
            "Here are the events you saved:",
            "The events you saved recently:"
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
    def ask_to_send_cv(cls):
        return random.choice([
            "Send me a copy of your resume (Y)",
            "Go ahead and me send your resume, %s ;)" % g.user.first_name
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
            "Whoop!",
            "Dang!"
        ])

    @classmethod
    def take_to_all_courses(cls):
        return random.choice([
            'Looking to improve your craft, %s?' % g.user.first_name[0],
            "You're eager to broaden your horizon... Awesome!",
            "Classes taught by people within your Blocs:",
            "Here are classes you could catch on Facebook:"])

    @classmethod
    def take_to_all_feeds(cls):
        return "Here's what is new on your Blocs"

    @classmethod
    def take_to_menu(cls):
        return "View everything across all your Blocs"

    @classmethod
    def ask_to_join_bloc(cls):
        return random.choice([
            "You have to join a Bloc first, %s!" % g.user.first_name[0],
            "Come on, %s. You haven't even joined a Bloc yet!" % (
                g.user.first_name),
            "%s, you have to pick a Bloc to join before you can view "
            "those..." % (g.user.first_name),
        ])


# if __name__ == '__main__':
#     print(Monologue.direct_to_checkout())
