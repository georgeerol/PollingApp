

# Schema
![schema](./misc/schema.png)
There's tree tables:
* `topic`    contains all the various topics we're going to be voting on.
            For example "*Is Alex Iwobi better than Dele Alli*".
* `option`  contains the voting options the users can choose when voting which would be(*Alex or Dele*)
* `polls`   serves as a `join` table(ManyToMany relationship)between topics and options,this table is needed
            because of the nature of the voting system where each option can belong to more than one topic at the same time.
            For example "*we can comparing Dele Alli to Messi at the same time as our first poll*". f we don’t do this we’ll end
            up creating several Dele Alli’s in our tables for the other topics where his name is used which would defeat the DRY principle.