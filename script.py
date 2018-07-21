"""
This module parses the standard input and prints the formatted output to the standard output
"""


import sys  # For reading the standard input


class FormatInput(object):
    """
        Class which has the implementation for parsing the standard input and printing the formatted output to the
        standard output
    """

    def __init__(self, out_prefix="*", out_block_prefix="."):
        """
            Constructor of the class
        :param out_prefix: Prefix for outline
        :param out_block_prefix: Prefix for outline block
        """
        self.out_prefix = out_prefix
        self.out_block_prefix = out_block_prefix
        self.outline_prefix_list = []
        self.parent_line = ""       # Will be used to check the previous line before formatting the current line
        self.outline_block_prefix_list = []
        self.prev_prefix_len = 0    # used for indentation of normal lines

    def format_and_print(self):
        """
            Method to format the standard input and print the formatted string to the standard output
        :return: None
        """
        for line in sys.stdin:
            if len(line.strip()) < 1: # Skip empty lines
                continue

            prefix_length, line = self.find_number_prefix_chars_and_substring(line, self.out_prefix)
            if prefix_length > 0:
                if len(self.parent_line):
                    # Print the last line of outline block
                    self.print_to_std_output(self.parent_line.replace("+", "-", 1))
                # Reset the outline block
                self.parent_line = ""
                self.outline_block_prefix_list = []

                # Format the outline and print
                formatted_line = self.format_outline(line, prefix_length)
                if formatted_line is not None:
                    self.print_to_std_output(formatted_line)
            else:
                prefix_length, line = self.find_number_prefix_chars_and_substring(line, self.out_block_prefix)
                formatted_line = self.format_outline_block(line, prefix_length)
                if formatted_line is not None:
                    self.print_to_std_output(formatted_line)

        if len(self.parent_line):
            # Print the last line of outline block
            self.print_to_std_output(self.parent_line.replace("+", "-", 1))

    def format_outline(self, line, prefix_length):
        """
            Method to format the outlines
        :param line: Line to be displayed after format
        :param prefix_length: Outline Prefix length
        :return:
        """
        if prefix_length > 0:
            if len(self.outline_prefix_list) == 0:
                self.outline_prefix_list.append(prefix_length)
            elif len(self.outline_prefix_list) >= prefix_length:
                self.outline_prefix_list = self.outline_prefix_list[:prefix_length]
                self.outline_prefix_list[prefix_length - 1] = self.outline_prefix_list[prefix_length - 1] + 1
            else:
                self.outline_prefix_list.append(1)

            prefix = ".".join(map(str, self.outline_prefix_list))
        else:
            return None

        return prefix + line

    def format_outline_block(self, line, prefix_length):
        """
            Method to format the outline block
        :param line: Line to be displayed after formatting
        :param prefix_length: Line Prefix length
        :return:
        """
        formatted_line = None
        if prefix_length > 0:
            self.prev_prefix_len = prefix_length  # used for indentation of normal lines
            if prefix_length not in self.outline_block_prefix_list:
                if len(self.parent_line):
                    formatted_line = self.parent_line
                self.parent_line = " " * (prefix_length + 1) + "+" + line
            else:
                if len(self.parent_line):
                    formatted_line = self.parent_line.replace("+", "-", 1)
                self.parent_line = " " * (prefix_length + 1) + "+" +  line
            self.outline_block_prefix_list.append(prefix_length)
        else:
            # Format normal lines
            self.parent_line += " " * (self.prev_prefix_len + 3) + line
        return formatted_line

    @staticmethod
    def find_number_prefix_chars_and_substring(actual_string, prefix_char):
        """
            Method to find the number of prefix characters and sub string
        :param actual_string: The line to be parsed
        :param prefix_char: The prefix character
        :return length, sub_string: Returns length of the prefix characters and sub string
        """
        length = len(actual_string.lstrip()) - len(actual_string.lstrip().lstrip(prefix_char))
        sub_string = actual_string.lstrip().lstrip(prefix_char)
        return length, sub_string

    @staticmethod
    def print_to_std_output(line):
        """
            Line to be send to standard output
        :param line: Formatted line
        :return: None
        """
        print line,


if __name__ == "__main__":
    format_obj = FormatInput()
    format_obj.format_and_print()
