def check(problem_input: str, output_user: str, output_judge: str) -> str:
    input_lines = problem_input.strip().splitlines()
    user_lines = output_user.strip().splitlines()
    judge_lines = output_judge.strip().splitlines()
    
    idx = 0
    t = int(input_lines[idx].strip()); idx += 1
    
    u_idx = 0
    j_idx = 0
    
    for tc in range(t):
        n = int(input_lines[idx].strip()); idx += 1
        p = list(map(int, input_lines[idx].split())); idx += 1
        d = list(map(int, input_lines[idx].split())); idx += 1
        
        if u_idx >= len(user_lines):
            return f"Test case {tc+1}: missing user output"
        if j_idx >= len(judge_lines):
            return f"Test case {tc+1}: missing judge output"
        
        user_line = user_lines[u_idx].strip(); u_idx += 1
        judge_line = judge_lines[j_idx].strip(); j_idx += 1
        
        judge_is_neg = judge_line.startswith('-1')
        user_is_neg = user_line.startswith('-1')
        
        if judge_is_neg:
            if not user_is_neg:
                return f"Test case {tc+1}: expected -1 but got {user_line}"
            continue
        else:
            if user_is_neg:
                return f"Test case {tc+1}: expected a valid permutation but got -1"
            
            try:
                q = list(map(int, user_line.split()))
            except:
                return f"Test case {tc+1}: cannot parse user output"
            
            if len(q) != n:
                return f"Test case {tc+1}: expected {n} integers, got {len(q)}"
            
            if sorted(q) != list(range(1, n+1)):
                return f"Test case {tc+1}: not a valid permutation of 1..{n}"
            
            # compute d from q and p
            for i in range(n):
                cnt = 0
                for j in range(i+1, n):
                    if p[j] > p[i] and q[j] > q[i]:
                        cnt += 1
                if cnt != d[i]:
                    return f"Test case {tc+1}: at index {i+1}, expected d={d[i]} but got {cnt}"
    
    return 'AC'
