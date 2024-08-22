from webtools.php import heredoc_string

def test_it_generates_correct_heredoc_string():
    assert "(<<<_\n\\163\\171\\163\\164\\145\\155\n_)" == heredoc_string("system")
