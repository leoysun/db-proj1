**COMS4111 Project 2 README**
December 6, 2024
Leo Sun UNI: lys2121
Julia Ding UNI: jld2251

PostgreSQL account: jld2251

____________________________________
Feature #1:
Text attribute

Implementation:
ALTER TABLE posts_reviews
ALTER COLUMN description TYPE TEXT;

Here, we do a very natural implementation of the TEXT data type into our schema. The "description" attribute contains the content of user reviews for food items. By making review content of type TEXT, not only are there less restrictions on character limits, but a potential feature of full-text searching through a database of reviews for keywords becomes easier and more streamlined. This is a very useful change that fits into the one of the goals of our project: to make the reviews more insightful and more accessible. 


Query:
SELECT d.dhall_name, pr.description
FROM posts_reviews pr
JOIN discusses d 
ON d.rid = pr.rid
WHERE to_tsvector(description) @@ to_tsquery('english', 'flavor');

This interesting query gives the review content and dining hall being reviewed for each review containing the word "flavor." This query might be conducted by someone looking for thoughtful reviews evaluating the actual taste of the food in a helpful manner, avoiding many reviews that superficially discuss personal emotion. 


____________________________________
Feature #2: 
Array attribute

Implementation:
ALTER TABLE has_item
ALTER COLUMN ingredients TYPE VARCHAR(30)[]
USING string_to_array(ingredients, ', ');

We implemented an array attribute in a very natural manner too. Previously, the 'ingredients' column in the Has_item table was just a varchar attribute implemented by comma-separated ingredient names. That was difficult to work with, and each individual ingredient could not easily be retrieved. With this change, each item can be accessed by its index in the array. Also, organization becomes easier — for example, I used the following SQL statement to sort all arrays of ingredients for each row in the table alphabetically:

UPDATE has_item
SET ingredients = (
    SELECT array_agg(elem ORDER BY elem)
    FROM unnest(ingredients) AS elem
);


Query:

SELECT dhall_name, item_name
FROM Has_item
WHERE dietary_info = 'Vegetarian'
  AND ('Cheese' = ANY(ingredients) OR 'Parmesan' = ANY(ingredients) OR 'Mozzarella' = ANY(ingredients)) 
  AND date > '2024-10-03';

This query finds all vegetarian items that contain cheese, parmesan, or mozzarella from after October 3, 2024. This may be used by a user who wants to find out which dining halls most regularly produce food that fits their appetite in a rather recent time frame. The array attribute is crucial here, allowing the ANY() function to access each item precisely and allowing the query to target specific items. 

Bonus query: 
This is another intersting query that aggregates and finds a list of unique ingredients from all dishes in the database using the neat unnest() function for the array.
SELECT DISTINCT unnest(ingredients) AS unique_ingredient
FROM Has_item
ORDER BY unique_ingredient;


____________________________________
Feature #3:
Trigger

We added a trigger on the Posts_reviews table to model the total participation constraint between Reviews entity set and the Discusses relationship set. After insertion into the posts_reviews table, the trigger calls a function to check whether the rid was correctly simultaneously inserted into the Discusses table (in one transaction). If the rid of the new review does not exist in the Discusses table, the function then deletes the new review. This way, the total participation constraint is enforced appropriately; no review can exist without discussing a certain item. 


Implementation: 

CREATE OR REPLACE FUNCTION reject_insert() RETURNS TRIGGER AS $$
BEGIN
	IF NOT EXISTS (SELECT 1 FROM Discusses d WHERE d.rid = NEW.rid)
	THEN DELETE FROM posts_reviews pr
	WHERE pr.rid = NEW.rid;
	RAISE EXCEPTION 'Insert rejected: rid does not exist in Discusses table';
END IF;
	RETURN NULL;
END;
$$ language plpgsql;

CREATE CONSTRAINT TRIGGER TotalPartRevItem
AFTER INSERT OR UPDATE ON Posts_reviews
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION reject_insert();


Example event: 

INSERT INTO posts_reviews
VALUES ('lys2121','2024-12-06', 'R11', 'Test review entry');

As a result, the trigger activates, checks that R11 is not an rid that exists in the Discusses table, and deletes the inserted tuple from the Posts_reviews table. Additionally, it raises the following exception:

ERROR:  Insert rejected: rid does not exist in Discusses table
CONTEXT:  PL/pgSQL function reject_insert() line 6 at RAISE

To summarize, the main modification to the database is the **deletion of the invalid newly inserted tuple**. 
