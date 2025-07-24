def find_symmetric_around(s: str, center: str) -> tuple[str, str]:
    if center not in s:
        return "", 0
    idx = s.find(center)
    max_len = min(idx, len(s) - idx - 1)
    print(max_len)
    result_list = []
    for l in range(max_len, 0, -1):
        left = s[idx - l:idx]
        right = s[idx + 1:idx + 1 + l]
        if left == right:
            result_list.append(left)
    print(result_list)
    if result_list:
        result = max(result_list, key=len)
        return result, idx
    re_detect, new_index = find_symmetric_around(s[idx + 1:], center)
    print(re_detect)
    if not re_detect:
        return "", 0
    return re_detect, new_index + idx + 1

# text = "不aa时aa不aa宇喵的aa"
# print("isornot")
# split_str, index = find_symmetric_around(text, "不")
# print(split_str)
# print(len(split_str))
# if not split_str:
#     quit()
# prefix = text[:index - len(split_str)]
# suffix = text[index + 1 + len(split_str):]
# print(prefix, suffix)
# splits = [prefix + split_str + suffix, prefix + "不" + split_str + suffix]
# print(splits)