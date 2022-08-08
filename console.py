#!/usr/bin/python3
"""Console module contain class HBNBCommand"""
import cmd


class HBNBCommand(cmd.Cmd):
    classes = {"BaseModel", "State", "City",
               "Amenity", "Place", "Review", "User"}

    def do_EOF(self, line):
        """
            Exit on Ctrl-D
        """
        print()
        return True

    def do_quit(self, line):
        """
            Exit on quit : quit
        """
        return True

    def emptyline(self):
        """
            Overwrite default behavior to repeat last command
        """
        pass

    def do_create(self, line):
        """
            Create instance specified by user : create User
        """
        if len(line) == 0:
            print("** class name missing **")
        elif line not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            instance = eval(line)()
            instance.save()
            print(instance.id)

    def do_show(self, line):
        """
            Print string representation: class name and id : show User id
        """
        if len(line) == 0:
            print("** class name missing **")
            return
        args = parse(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        try:
            if args[1]:
                name = f"{args[0]}.{args[1]}"
                if name not in storage.all().keys():
                    print("** no instance found **")
                else:
                    print(storage.all()[name])
        except IndexError:
            print("** instance id missing **")

    def do_destroy(self, line):
        """
            Destroy instance specified by user; Save changes to JSON file
                                    destroy User id
        """
        if len(line) == 0:
            print("** class name missing **")
            return
        args = parse(line)
        if args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        try:
            if args[1]:
                name = f"{args[0]}.{args[1]}"
                if name not in storage.all().keys():
                    print("** no instance found **")
                else:
                    del storage.all()[name]
                    storage.save()
        except IndexError:
            print("** instance id missing **")

    def do_all(self, line):
        """
            Print all objects or all objects of specified class
                    all  -> for all Objects
                    all User  -> for User objects only
        """
        args = parse(line)
        if len(line) == 0:
            obj_l = [objs for objs in storage.all().values()]
            print(obj_l)
        elif args[0] in HBNBCommand.classes:
            obj_l = [objs for key, objs in storage.all().items()
                     if args[0] in key]
            print(obj_l)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """
            Update if given exact object, exact attribute
                   update User id attribute value
        """
        args = parse(line)
        if len(args) >= 4:
            key = f"{args[0]}.{args[1]}"
            cast = type(eval(args[3]))
            arg3 = args[3]
            arg3 = arg3.strip('"')
            arg3 = arg3.strip("'")
            setattr(storage.all()[key], args[2], cast(arg3))
            storage.all()[key].save()
        elif len(args) == 0:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif (f"{args[0]}.{args[1]}") not in storage.all().keys():
            print("** no instance found **")
        elif len(args) == 2:
            print("** attribute name missing **")
        else:
            print("** value missing **")

    def do_count(self, line):
        """
            Display count of instances specified : count User
        """
        if line in HBNBCommand.classes:
            count = 0
            for key, objs in storage.all().items():
                if line in key:
                    count += 1
            print(count)
        else:
            print("** class doesn't exist **")

    def default(self, line):
        """
            Accepts class name followed by argument
        """
        args = line.split('.')
        class_arg = args[0]
        if len(args) == 1:
            print(f"*** Unknown syntax: {line}")
            return
        try:
            args = args[1].split('(')
            command = args[0]
            if command == 'all':
                HBNBCommand.do_all(self, class_arg)
            elif command == 'count':
                HBNBCommand.do_count(self, class_arg)
            elif command == 'show':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip("'")
                id_arg = id_arg.strip('"')
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_show(self, arg)
            elif command == 'destroy':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip('"')
                id_arg = id_arg.strip("'")
                arg = class_arg + ' ' + id_arg
                HBNBCommand.do_destroy(self, arg)
            elif command == 'update':
                '''
                args = args[1].split(',')
                id_arg = args[0].strip("'")
                id_arg = id_arg.strip('"')
                '''
                args = args[1].split('{')
                id_arg = args[0].strip(' ').strip(',').strip('"').strip("'")
                print(id_arg)
                attr_args = args[1].rstrip(')').rstrip('}')
                attr_args = '{' + attr_args + '}'
                attr_args = attr_args.replace("'", '"')
                attr_args = json.loads(attr_args)
                for k, v in attr_args.items():
                    arg = f"{class_arg} {id_arg} {k} {v}"
                    print(arg)
                    # HBNBCommand.do_update(self, arg)
                '''
                name_arg = args[1].split(':')[0].strip('"').strip('"')
                name_arg = name_arg.strip(' ').strip('{').strip('"').strip("'")
                print(name_arg)
                val_arg = args[1].split(':')[1].strip(' ')
                print(val_arg)
                arg = class_arg + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                HBNBCommand.do_update(self, arg)
                name_arg = args[2].split(':')[0].strip('"').strip('"')
                name_arg = name_arg.strip(' ').strip('{').strip('"').strip("'")
                print(name_arg)
                val_arg = args[2].split(':')[1].split('}')[0].strip(' ')
                print(val_arg)
                arg = class_arg + ' ' + id_arg + ' ' + attr_arg + ' ' + val_arg
                HBNBCommand.do_update(self, arg)
                '''
            else:
                print(f"*** Unknown syntax: {line}")
        except IndexError:
            print(f"*** Unknown syntax: {line}")


def parse(line):
    """Helper method to parse user typed input"""
    return tuple(line.split())

if __name__ == '__main__':
    HBNBCommand().cmdloop()
