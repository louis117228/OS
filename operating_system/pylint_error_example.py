class foo:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def show_name(self):
        print(self.name)

    def get_name(self):
        return self.name

    def priority_cmp(self):
        global priority_max
        if (self.priority > priority_max):
            priority_max = self.priority

    def get_priority(self):
        return self.priority

foo_num = int(input('please key in foo num:'))
foo_list = []
priority_max = 0

for i in range(foo_num):
    i += 1
    my_foo = foo(name = 'foo%d' % i, priority = i + 2)
    foo_list.append(my_foo)

for i in range(foo_num):
    print(foo_list[i])
    print('name',foo_list[i].get_name())
    foo_list[i].priority_cmp()
    print('priority_max',priority_max)