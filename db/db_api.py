
            User.update('kay', 'abc', 'bear', 'bear@gmail.com', 'M', '30/01/1999', 'Bear is bear', 'picture')
            details = User.find('kay')
        except UserNotFound:
            pass
        multidetails = User.find_multiple()
#Georges
        my_user = User.sign_up('amazing-user', 'secure-password', '¯\_(ツ)_/¯', 'some@email.com', '1/10/2017')

        # -- Begin Post testing
        print_w("Beginning Post tests")

        my_post = Post.create(my_user.id, "Can y'all help me with finding out where I can get this water bottle from (and what brand it is)?", "What's this water bottle?", "1/10/2017", [])
        # Post finding testing
        assert Post.find(my_post.id).user_id == my_user.id  # Expected result: Pass
        print_p("Existing Post finding test passed!")
        try:
            Post.find(999) # Expected result: Fail
            assert 0
        except PostNotFound:
            print_p("Uncreated Post finding test passed!")
        # Post deleting testing
        Post.delete(my_post.id)
        try:
            Post.find(my_post.id) # Expected result: Pass
            assert 0
        except PostNotFound:
            print_p("Post deleting test passed!")
        print()
        print_p("Post tests passed!")

        # -- End Post testing
