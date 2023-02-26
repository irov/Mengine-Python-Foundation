# class Linked(object):
#     __slot__ = "root", "last"
#
#     class Node(object):
#         __slot__ = "value", "next"
#
#         def __init__(self, value):
#             self.value = value
#             self.next = None
#             pass
#
#         def link(self, node):
#             node.next = self.next
#             self.next = node
#             pass
#         pass
#
#     def __init__(self):
#         self.root = None
#         self.last = None
#         pass
#
#     def append(self, value):
#         node = Linked.Node(value)
#
#         if self.last is None:
#             self.root = node
#             self.last = node
#             pass
#         else:
#             self.last.link(node)
#             self.last = node
#             pass
#         pass
#
#     def remove(self, value):
#         if self.root is None:
#             raise ValueError("Linked empty for remove %s"%(value))
#             pass
#
#         if self.root.value == value:
#             if self.last is self.root:
#                 self.root = None
#                 self.last = None
#                 pass
#             else:
#                 self.root = self.root.next
#                 pass
#
#             return
#             pass
#
#         node = self.root
#         while node.next is not None:
#             if node.next.value != value:
#                 node = node.next
#                 continue
#                 pass
#
#             if self.last is node.next:
#                 self.last = node
#                 pass
#
#             node.next = node.next.next
#
#             break
#             pass
#         pass
#
#     def empty(self):
#         return self.root is None
#         pass
#
#     def copy(self):
#         L = Linked()
#
#         for value in self:
#             L.append(value)
#             pass
#
#         return L
#         pass
#
#     def __len__(self):
#         count = 0
#         node = self.root
#         while node is not None:
#             count += 1
#             node = node.next
#             pass
#
#         return count
#         pass
#
#     def __contains__(self, value):
#         node = self.root
#         while node is not None:
#             if node.value == value:
#                 return True
#                 pass
#
#             node = node.next
#             pass
#
#         return False
#         pass
#
#     def __iter__(self):
#         node = self.root
#         while node is not None:
#             yield node.value
#             node = node.next
#             pass
#         pass
#     pass