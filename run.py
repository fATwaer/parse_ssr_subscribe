from blessed import Terminal
import parse

term = Terminal()
print(f"{term.home}{term.clear}")

parse.display_all_server_nodes(parse._CONFIG)

print("press 'q' to quit.")
with term.cbreak():
    val = ''
    while val.lower() != 'q':
        val = term.inkey(timeout=3)
        if not val:
           print("It sure is quiet in here ...")
        elif val.is_sequence:
           print("got sequence: {0}.".format((str(val), val.name, val.code)))
        elif val:
           print("got {0}.".format(val))
    print(f'bye!{term.normal}')
