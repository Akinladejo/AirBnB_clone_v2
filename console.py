#!/usr/bin/python3
"""This module defines the HBNBCommand class, a subclass of cmd.Cmd"""
import cmd
from models.engine.db_storage import storage


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class for the command interpreter"""

    prompt = '(hbnb) '

    def do_EOF(self, line):
        """Exit the program"""
        return True

    def emptyline(self):
        """Do nothing on empty input"""
        pass

    def do_quit(self, line):
        """Quit the program"""
        return True

    def do_create(self, arg):
        """Create a new instance of BaseModel"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.all().keys():
            print("** class doesn't exist **")
            return
        new_instance = eval(args[0])()
        new_instance.save()

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.all().keys():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.all().keys():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances"""
        args = arg.split()
        objs = []
        if len(args) == 0:
            for obj in storage.all().values():
                objs.append(str(obj))
            print(objs)
        else:
            if args[0] not in storage.all().keys():
                print("** class doesn't exist **")
                return
            for key, obj in storage.all().items():
                if args[0] in key:
                    objs.append(str(obj))
            print(objs)

    def do_update(self, arg):
        """Updates an instance based on the class name and id"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.all().keys():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = "{}.{}".format(args[0], args[1])
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        obj = storage.all()[key]
        setattr(obj, args[2], args[3])
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
