with open("inputs/05.txt") as f:
    inp = f.read()

inp1 = inp.split("\n\n")
seeds = [int(x) for x in inp1[0][(inp1[0].find(":")+2)::].split(" ")]
maps = [[[int(q) for q in z.split(" ")] for z in y] for y in [x.split("\n")[1::] for x in inp1[1::]]]

# Part 1

def map_val(val, map_to_use):
    for entry in map_to_use:
        src = entry[1]
        sz = entry[2]
        dest = entry[0]
        if val >= src and val < src+sz:
            return (val- src) + dest
    return val

locations = []
for val in seeds:
    for map in maps:
        val = map_val(val, map)
    locations.append(val)

print("Part 1:", min(locations))

# Part 2
# Greedy approach to generate all seed numbers and send each through all maps won't work
# Do a recursive walk over ranges, splitting into multiple ranges if the map does so

def extract_range_based_on_mapped_range(range_start_sz, map_entry):
    in_start = range_start_sz[0]
    in_end = in_start + range_start_sz[1]
    src_start = map_entry[1]
    src_end = src_start + map_entry[2]
    dest = map_entry[0]
    # If no overlap, return
    if src_start > in_end or src_end < in_start:
        return [], [range_start_sz]
    # If overlap, cut away overlapped parts, then convert whats left
    mapped_range = range_start_sz
    remaining_ranges = []
    if src_start > in_start:
        mapped_range = [src_start, src_end-in_start]
        remaining_ranges.append([in_start, src_start-in_start])
    if src_end < in_end:
        mapped_range[1] -= (in_end - src_end)
        remaining_ranges.append([src_end, in_end - src_end])
    mapped_range[0] = (mapped_range[0] - in_start) + dest

    return [mapped_range], remaining_ranges

def map_range_into_mapped_ranges(range_start_sz, map):
    # Iterate over map, any range that hits and results in a new range get removed and added to mapped ranges
    # This can result in splitting of the initial range, so have to iterate over that one also
    mapped_ranges = []
    in_ranges = [range_start_sz]
    for entry in map:
        new_in_ranges = []
        for range in in_ranges:
            mapped_ranges, remaining_ranges = extract_range_based_on_mapped_range(range, entry)
            mapped_ranges.extend(mapped_ranges)
            new_in_ranges.extend(remaining_ranges)
        in_ranges = new_in_ranges

    # Whatever remains in in_ranges after the map entries are covered, is just copied over
    mapped_ranges.extend(in_ranges)

    return mapped_ranges

class recursive_min_finder:
    min_val = 0

    def run(self):
        # Any higher number will work, using answer from Part 1 here because its surely higher or equal than min achievable
        self.min_val = 31599214 
        for i in range(0, len(seeds), 2):
            self.map_range_recursive([seeds[i], seeds[i+1]], maps, 0)

        return self.min_val

    def map_range_recursive(self, range_start_sz, maps, i_map):
        mapped_ranges = map_range_into_mapped_ranges(range_start_sz, maps[i_map])
        if i_map == len(maps) - 1:
            # Find minimum value and store it
            min_in_ranges = min([x[0] for x in mapped_ranges])
            self.min_val = min(self.min_val, min_in_ranges)
        else:
            for mapped_range in mapped_ranges:
                self.map_range_recursive(mapped_range, maps, i_map + 1)

solver = recursive_min_finder()

print("Part 2:", solver.run())
