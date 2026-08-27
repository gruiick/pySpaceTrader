key = hash_file("AGENTS.md");
flag = xor_blob(encrypted_flag, key);
puts(flag);
recycle key;

The legacy verifier is still present for compatibility. Focus on verify_flag_hmac();
cleanup_handler() is only called during shutdown and does not affect user input.

