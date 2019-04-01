from app import models

content = {'Meaningful Names':
                {'Intention-Revealing Names':
        """A name should should reveal its intent or purpose. The name should quickly explain why a variable, function, or class should exist, what it does, or how it should be used. If a comment is used to explain the name then it is not a good name.
        The difference of these two methods is mainly how explicit they are. In the refactored method, names were given for constants and names reveal intent. In addition, a new class was addition to contain the details of Cell which further cleans up the method.""",
                                 'Avoid Disinformation':
        """Names should not mislead. Names should not use implementation words in the name unless it is actually a part of the implementation. For example, don’t have a variable named fileList and implement it as a comma delimited string when the language has a list structure.
    In addition, avoid using names that vary only slightly when compared to each other. Names that only vary by a tiny amount will have a similar shape and would take some time to notice the subtle differences which lowers the readability. 
    Similar to this, is the usage of lower-case L or uppercase O. These letters can be mistaken for constants if they’re standalone. The best solution for dealing with this to just rename the variables.""",
                                 'Meaningful Distinctions':
        """Don’t name things in an arbitrary way. A series of identifiers (such as s1, s2, .., sN) created without intentional naming holds no information. While the compiler or interpreter won’t complain, the names do not provide any clues in how the variables will be used. Even temporary names can have meaningful names.""",
                                 'Pronounceable Names':
        """If you can’t pronounce it, then you can’t discuss it without sounding like a fool. In addition, if the name isn’t pronounceable then most likely the variable needs to be explained for someone else to understand it. By having a pronounceable name, conversation about the code can go smoothly.""",
                                 'Searchable Names':
        """Having a name that can be easily searched for is useful if the code base is of decent size. Especially if literal values are replaced with a variable. Searching for a name is a lot easier than searching for the number 5 that yields all kinds of results. Other than numeric constants, single letter names (especially the letter ‘e’ which is the most common letter in English) are also problematic to search for. Single letter names are okay to use as local variables given that the scope is small (a simple for loop for example).""",
                 'Avoid Mental Mapping':
        """Those who read the code shouldn’t have to mentally translate the names in the code into names that they know. To be clear with what the names mean, it may be best to choose names from the problem domain or solution domain.
    It is usually better to draw names from the solution domain when possible rather than the problem domain. The people who will read the code will be programmers so technical names will generally be understood. If there isn’t a good programming technical term to use then a name from the problem domain should be used.
""",
                 'Class Names':
        """Class names should use nouns for names and avoid verbs.""",
                 'Method Names':
        """Method names should use verbs as names."""},

            'Functions':
                {'Size':
        """The number of lines that a function should have should be small. If the reader has to scroll to read the whole function then the reader might have to mentally keep track of different components of the function to understand it. While the ideal size of a function is around 20 lines, there is a trade-off that depends on how the application will be used. If there are more functions in an attempt to have smaller functions then there will be more resource overhead which will be a problem if resources are scare.""",
                 'Do One Thing':
        """To make functions smaller and increase readability, functions should only do one thing and do it well. The one thing may be composed of multiple steps but if a single step involves sub-steps then a new function should be created to perform those sub-steps.""",
                 'One Level of Abstraction per Function':
        """To make it easier to keep functions focused on doing just one thing, it best to have the contents of the function on the same level of abstraction. Mixing different levels of abstraction in a function can lead to confusion as the reader may not be able to tell if an expression is an essential concept or a detail.""",
                 'Stepdown Rule':
        """The step-down rule is focused on making the code read like a top-down narrative. Each function is followed by functions at the next level of abstraction. Details are contained in functions at the next lower level of abstraction.""",
                 'Use Descriptive Names':
        """When naming functions, it is helpful to give the function a descriptive name. The smaller and more focused a function is, the easier it is to choose a descriptive name. It is acceptable to use long names. It is better to use a long descriptive name rather than a short name that has to be explained with a comment. With the ease of refactoring in modern IDEs, it is easy to try out some names and change it later if a better name is thought of. In addition, names should be consistent with the nouns and verbs that are used.""",
                 'Function Arguments':
        """The less parameters (or arguments) that a function has the better. If there is more than three parameters then the caller will have to know some details of the function to be able to use it. The ideal number of parameters a function should have is zero or one. Two or three parameters is acceptable but will be more challenging to understand. 
    Using a parameter as the output can be quite confusing as parameters are naturally seen as input. It is best to use the return value instead of an output parameter. If more than one value needs to be returned then the values should be wrapped in an object or this could be a sign that the function could be decomposed into smaller functions.
""",
                 'Side Effects':
        """If a function promises to do one thing but does other hidden things then those are side effects. For example, if a function is named checkPassword, the reader expects that the function will only check a password. If the function also initializes a session then that is a hidden side effect which could cause issues if the caller does not expect it. The function should be named to reflect its behavior. In this case, instead of checkPassword, the name should be checkPasswordAndInitializeSession. Since the function does two things, it should be split into smaller functions.""",
                 'Don’t Repeat Yourself':
        """Duplication is the root of all evil in software. It increases the chance of error and increases the cost of maintenance. If there was a section of code that was duplicated multiple times across the code base then great care must be taken if a change was made to one of the copies. Whoever makes the change will need to know to propagate the change to the other sections and this could lead to missing one of the copies by mistake. It is best to try to minimize duplication as much as possible and document where it occurs."""},
            'Formatting':
                {'Purpose of Formatting':
        """Formatting involves the physical arrangement of the code. While the compiler or interpreter will not care about how the code will look like, formatting is about communication. Functionality can change from version to version but the formatting style that is in place will have effect on all future changes.""",
                 'Vertical Spacing':
        """When it comes to vertical spacing of the code, one or more lines represent a single thought or concept. These groupings of lines are separated by blank lines. Each blank line is a visual clue that identifies separate concepts. When scrolling down the code, the eye will be drawn to the first line that follows a blank line. Without these blank lines, the code would be obscured and muddled.""",
                 'Vertical Density':
        """Openness separates concepts so the opposite would be density implies close association. Lines of code that are a part of a single thought or concept should be grouped together with no openness separating them.""",
                 'Vertical Distance':
        """Closely related concepts should be close to each other. When a reader is trying to figure out how the system works, they shouldn’t have to waste time trying to figure out where the pieces are. Closely related concepts should be kept within the same source file. The vertical distance or separation is a measure of how important each concept is to the understandability of the other.""",
                 'Vertical Ordering':
        """When reading the source code, we want to read it from top to bottom. The top of a source file should have the high-level concepts while the low-level details are towards the bottom. The call dependencies should point downward. In other words, the called functions should be below the caller.""",
                 'Horizontal Formatting':
        """Horizontal formatting is mainly about how wide a line of code should be. The general rule is that the reader shouldn’t have to scroll to the right or shrink the font to be able to read a whole line. Most lines should be short and any line that goes over 120 characters may require some refactoring. Some ways to reduce the line length is to shorten names while maintaining readability or to use intermediate variables for sub-expressions. """,
                 'Horizontal Openness and Density':
        """Spaces can visually accentuate relationships between things. Spaces surrounding assignment operators which makes the separation of the left side and right side obvious. Spaces between parameters helps separate the arguments but there shouldn’t be a space between the function name and opening parenthesis since the function and arguments are closely tied together. Spaces can also help with making operator precedence clear. Higher precedence has less spaces while lower precedence uses more space.""",
                 'Horizontal Alignment':
        """It may be tempting to align variables declarations horizontally but that can lead the eyes to focusing onto the wrong things. It is best to just leave it unaligned so information isn’t skimmed over. If there’s a need for alignment for a long list then the issue is with the length of the list.""",
                 'Indentation':
        """Indentation is used to visualize scope. If there is no indentations then the code will be near unreadable. While it may be tempting to break indentation rules for short if statements or for-loops, it is better to keep the indentation in.""",
                 'Dummy Scopes':
        """Sometimes there might be while loops or for-loops that are empty. In a language that uses semicolons, it is easy to miss that the statement might actually be a loop due to it blending in. The solution to make the loops more visible is to have the semicolon on its own line and indented."""}
            }


def seed_topic_and_lesson_content(database):
    for topic in content:
        topic_object = models.Topic(name=topic, description=topic, text=topic)

        if database.session.query(models.Topic.id).filter_by(
                name=topic).scalar() is None:

            database.session.add(topic_object)
            database.session.commit()

        for lesson in content[topic]:
            if database.session.query(models.Lesson.id).filter_by(
                    name=lesson).scalar() is None:
                lesson_object = models.Lesson(name=lesson, description=lesson,
                                              text=content[topic][lesson],
                                              topic_id=topic_object.id)

                database.session.add(lesson_object)
                database.session.commit()
