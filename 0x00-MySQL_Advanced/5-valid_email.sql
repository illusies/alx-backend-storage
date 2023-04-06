-- A SQL script that creates a trigger that resets
-- the attribute valid_email only when the email has
-- been changed.
CREATE TRIGGER reset_attrib;
AFTER UPDATE ON users
FOR EACH ROW 
BEGIN
 IF NEW.email != OLD.email THEN
   UPDATE users SET valid_email=NULL;
 END IF;
END;
