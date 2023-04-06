-- A SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes and store
-- the average weighted score for a student
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
  user_id INT)
BEGIN
  DECLARE aw_score FLOAT;
  SET aw_score = (SELECT SUM(score * weight) / SUM(weight)
    FROM users AS set_U 
    JOIN corrections as set_C ON set_U.id=set_C.user_id 
    JOIN projects AS set_P ON set_C.project_id=set_P.id 
    WHERE set_U.id=user_id);
  UPDATE users SET average_score = aw_score WHERE id=user_id;
END;
//
