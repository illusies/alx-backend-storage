-- A SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUser that computes and store
-- the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS set_U, 
    (SELECT set_U.id, SUM(score * weight) / SUM(weight) AS w_avg 
    FROM users AS set_U 
    JOIN corrections as set_C ON set_U.id=set_C.user_id 
    JOIN projects AS set_P ON set_C.project_id=set_P.id 
    GROUP BY set_U.id)
  AS set_WA
  SET set_U.average_score = set_WA.w_avg 
  WHERE set_U.id=set_WA.id;
END;
//
