const std = @import("std");

fn printBoard(board: *const *[9][9]u8) void {
    for (0..9) |i| {
        for (0..9) |j| {
            const val = board.*[i][j];
            if (val == 0) std.debug.print("_", .{}) else std.debug.print("{}", .{val});
        }
        std.debug.print("\n", .{});
    }
}

fn isSolution(board: *const *[9][9]u8) bool {
    for (0..9) |i| {
        var line = std.bit_set.IntegerBitSet(10).initEmpty();
        for (0..9) |j| {
            const val = board.*[i][j];
            if (val == 0) {
                return false;
            }

            if (line.isSet(val)) {
                return false;
            }
            if (val != 0) {
                line.set(val);
            }
        }
        if (line.count() != 9) {
            return false;
        }
    }
    return true;
}

fn isCandidate(board: *const *[9][9]u8, i: usize, j: usize, new_val: usize) bool {
    if (board.*[i][j] != 0) {
        return false;
    }

    // row
    for (0..9) |k| {
        if (k == i) continue;

        const val = board.*[k][j];
        if ((val != 0) and (val == new_val)) {
            return false;
        }
    }

    // col
    for (0..9) |k| {
        if (k == j) continue;

        const val = board.*[i][k];
        if ((val != 0) and (val == new_val)) {
            return false;
        }
    }

    // quadrant
    const qi = i / 3 * 3;
    const qj = j / 3 * 3;
    for (qi..qi + 3) |ki| {
        for (qj..qj + 3) |kj| {
            if ((ki == i) and (kj == j)) continue;

            const val = board.*[ki][kj];
            if (val == new_val) {
                return false;
            }
        }
    }

    return true;
}

fn slowSolve(board: *[9][9]u8) bool {
    if (isSolution(&board)) return true;

    for (0..9) |i| {
        for (0..9) |j| {
            const val = board[i][j];
            if (val != 0) continue; // position already set

            for (1..10) |new_val| {
                if (isCandidate(&board, @intCast(i), @intCast(j), @intCast(new_val))) {
                    board[i][j] = @intCast(new_val);
                    if (slowSolve(board)) return true;
                    board[i][j] = val;
                }
            }
        }
    }
    return false;
}

const Candidate = struct {
    i: usize,
    j: usize,
    val: usize,

    pub fn format(self: @This(), comptime _: []const u8, _: std.fmt.FormatOptions, writer: anytype) std.os.WriteError!void {
        return writer.print("<i={}, j={}, val={}>", .{ self.i, self.j, self.val });
    }
};

fn solveLookAhead(board: *[9][9]u8) bool {
    if (isSolution(&board)) return true;

    var best_count: usize = 10;
    var best_candidates: [9]Candidate = [_]Candidate{.{ 0, 0, 0 }} ** 9;
    for (0..9) |i| {
        for (0..9) |j| {
            if (board[i][j] != 0) continue; // position already set

            var candidates: [9]Candidate = [_]Candidate{.{ 0, 0, 0 }} ** 9;
            var cur_count: usize = 0;
            for (1..10) |val| {
                if (isCandidate(&board, i, j, val)) {
                    candidates[cur_count] = .{ .i = i, .j = j, .val = val };
                    cur_count += 1;
                }
            }
            if (cur_count == 0) return false;
            if (cur_count < best_count) {
                best_count = cur_count;
                for (0..cur_count) |k| {
                    best_candidates[k] = candidates[k];
                }
            }
        }
    }

    if (best_count == 10) return false; // no candidates

    for (0..best_count) |idx| {
        // std.debug.print("{}\n", .{best_candidates[idx]});
        const i = best_candidates[idx].i;
        const j = best_candidates[idx].j;
        const old_val = board[i][j];
        board[i][j] = @intCast(best_candidates[idx].val);
        if (solveLookAhead(board)) return true;
        board[i][j] = old_val;
    }

    return false;
}

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    const stdin = std.io.getStdIn().reader();

    var text: [90]u8 = undefined;
    _ = try stdin.read(&text);

    var board = [9][9]u8{
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
        [_]u8{ 0, 0, 0, 0, 0, 0, 0, 0, 0 },
    };

    var lines = std.mem.splitScalar(u8, &text, '\n');
    for (0..9) |i| {
        const line = lines.next().?;
        for (0..9) |j| {
            board[i][j] = try std.fmt.parseInt(u8, line[j .. j + 1], 10);
        }
    }

    std.debug.print("------Starting Board------\n", .{});
    printBoard(&&board);
    std.debug.print("------Solution------\n", .{});

    const start = std.time.nanoTimestamp();
    // const res = slowSolve(&board);
    const res = solveLookAhead(&board);
    const end = std.time.nanoTimestamp();
    if (!res) {
        std.debug.print("no solution", .{});
        return;
    }

    for (0..9) |i| {
        for (0..9) |j| {
            try stdout.print("{}", .{board[i][j]});
        }
        try stdout.print("\n", .{});
    }
    std.debug.print("solve took {} seconds\n", .{@as(f64, @floatFromInt(end - start)) / 1e9});
}
