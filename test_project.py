import subprocess


def output_helper(input_command):
	return subprocess.check_output(input_command).decode("utf-8")


def test_word_in_one_file():
	cmd = ['grep', 'the', './files/reg_file1']
	res = output_helper(cmd)
	assert (res == "the ball\nthe wall\nthe mall\n")


def test_word_in_two_files():
	cmd = ['grep', 'grep', './files/reg_file3', './files/reg_file4']
	res = output_helper(cmd)
	assert (res == "./files/reg_file3:one grep\n./files/reg_file3:two greps\n./files/reg_file4:another grep\n./files/reg_file4:grep\n")


def test_empty_lines():
	cmd = ['grep', '-E', '-c', '^$', './files/reg_file2']
	res = output_helper(cmd)
	assert (res == '3\n')


def test_few_patterns():
	cmd = "grep 'second' './files/few_pat_file' | grep 'pattern'"
	res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	assert (res.communicate()[0].decode("utf-8") == 'The second line with pattern\n')


def test_negative():
	cmd = ['grep', 'Lorem ipsum', './files/reg_file1']
	try:
		res = output_helper(cmd)
	except subprocess.CalledProcessError as e:
		res = e.returncode
	assert (res == 1)


def test_regexp():
	cmd = ['grep', '-G', '[a-zA-Z].123\.', './files/regexp_file']
	res = output_helper(cmd)
	assert(res == "sfgkjhSGF123.\n")


def test_cyrillic():
	cmd = ['grep', 'на русском', './files/cyrillic_file']
	res = output_helper(cmd)
	assert(res == "Текст на русском языке\n")


def test_recursion():
	cmd = "grep -r recursive ./files/subdir"
	res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	assert (res.communicate()[0].decode("utf-8") == './files/subdir/subsubdir/recursive_file:Text for recursive check\n')
