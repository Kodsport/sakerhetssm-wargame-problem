const std = @import("std");

const flag = "SSM{D0wn_th3_ro4d_1_go!}";

noinline fn node(comptime target: []const u8, comptime right_path: bool, guesses: []const u8) bool {
    if(target.len == 0) {
        return right_path and guesses.len == 0;
    }

    if(guesses.len == 0) {
        return false;
    }

    if (target[0] == guesses[0]) {
        return node(target[1..], right_path, guesses[1..]);
    } else {
        return node(target[1..], false, guesses[1..]);
    }
}

pub fn main() anyerror!void {
    const stdin = std.io.getStdIn().reader();
    const stdout = std.io.getStdOut().writer();

    var input_buf: [64]u8 = undefined;

    try stdout.print("Please enter the flag: ", .{});

    if (try stdin.readUntilDelimiterOrEof(&input_buf, '\n')) |user_input| {
        if (node(flag, true, user_input)) {
            try stdout.print("Correct!\n", .{});
        } else {
            try stdout.print("Incorrect!\n", .{});
        }
    } else {
        return stdout.print("Failed to read input, exiting.\n", .{});
    }
}

test "basic test" {
    try std.testing.expectEqual(10, 3 + 7);
}
