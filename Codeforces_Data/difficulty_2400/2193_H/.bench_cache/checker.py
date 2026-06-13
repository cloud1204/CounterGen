def check(problem_input: str, output_user: str, output_judge: str) -> str:
    input_lines = problem_input.split('\n')
    user_lines = output_user.split('\n')
    judge_lines = output_judge.split('\n')
    
    idx_in = 0
    idx_user = 0
    idx_judge = 0
    
    def next_input_line():
        nonlocal idx_in
        while idx_in < len(input_lines) and input_lines[idx_in].strip() == '':
            idx_in += 1
        if idx_in >= len(input_lines):
            return None
        line = input_lines[idx_in]
        idx_in += 1
        return line
    
    def next_user_line():
        nonlocal idx_user
        while idx_user < len(user_lines) and user_lines[idx_user].strip() == '':
            idx_user += 1
        if idx_user >= len(user_lines):
            return None
        line = user_lines[idx_user]
        idx_user += 1
        return line
    
    def next_judge_line():
        nonlocal idx_judge
        while idx_judge < len(judge_lines) and judge_lines[idx_judge].strip() == '':
            idx_judge += 1
        if idx_judge >= len(judge_lines):
            return None
        line = judge_lines[idx_judge]
        idx_judge += 1
        return line
    
    try:
        t = int(next_input_line())
    except:
        return "Failed to parse number of test cases"
    
    for tc in range(1, t + 1):
        try:
            n = int(next_input_line())
            a = list(map(int, next_input_line().split()))
            if len(a) != n:
                return f"Test {tc}: input parsing error"
            adj = [[] for _ in range(n + 1)]
            for _ in range(n - 1):
                u, v = map(int, next_input_line().split())
                adj[u].append(v)
                adj[v].append(u)
        except Exception as e:
            return f"Test {tc}: failed parsing input: {e}"
        
        user_verdict = next_user_line()
        judge_verdict = next_judge_line()
        
        if user_verdict is None:
            return f"Test {tc}: user output missing verdict"
        if judge_verdict is None:
            return f"Test {tc}: judge output missing verdict"
        
        user_ans = user_verdict.strip().lower()
        judge_ans = judge_verdict.strip().lower()
        
        if user_ans not in ('yes', 'no'):
            return f"Test {tc}: invalid verdict '{user_verdict}'"
        
        if user_ans != judge_ans:
            return f"Test {tc}: user said '{user_ans}', judge said '{judge_ans}'"
        
        if judge_ans == 'yes':
            # judge has a sequence line
            judge_seq_line = next_judge_line()
            # user must also have a sequence
            user_seq_line = next_user_line()
            if user_seq_line is None:
                return f"Test {tc}: user said YES but no sequence given"
            try:
                seq = list(map(int, user_seq_line.split()))
            except:
                return f"Test {tc}: failed to parse user's sequence"
            
            if len(seq) != n:
                return f"Test {tc}: sequence length {len(seq)}, expected {n}"
            
            if sorted(seq) != list(range(1, n + 1)):
                return f"Test {tc}: sequence is not a permutation of 1..{n}"
            
            # Simulate removal
            removed = [False] * (n + 1)
            # Current neighbor sum for each vertex
            S = [0] * (n + 1)
            for v in range(1, n + 1):
                for u in adj[v]:
                    S[v] += a[u - 1]
            
            for v in seq:
                if removed[v]:
                    return f"Test {tc}: vertex {v} already removed"
                # Check parity differs
                if (a[v - 1] % 2) == (S[v] % 2):
                    return f"Test {tc}: cannot remove vertex {v}, a_v={a[v-1]} S_v={S[v]} have same parity"
                # Remove v: update neighbors
                removed[v] = True
                for u in adj[v]:
                    if not removed[u]:
                        S[u] -= a[v - 1]
            
        # else NO, nothing extra to read
    
    return 'AC'
